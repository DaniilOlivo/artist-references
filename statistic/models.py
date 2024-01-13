from django.db import models
from django.contrib.auth.models import User
from references.models import Tag
from django.db.models.signals import post_save
from django.dispatch import receiver

class StatisticsBase (models.Model):
    attempts = models.IntegerField(default=0)
    images = models.IntegerField(default=0)
    new = models.IntegerField(default=0)
    fail = models.IntegerField(default=0)
    error = models.IntegerField(default=0)
    success = models.IntegerField(default=0)
    masterpiece = models.IntegerField(default=0)

    class Meta:
        abstract = True

class StatisticsTotal (StatisticsBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics')
    def __str__(self):
        return self.user.username + " statistics"
    
class StatisticsTag (StatisticsBase):
    tag = models.OneToOneField(Tag, on_delete=models.CASCADE, related_name='statistics')

    def __str__(self):
        return self.tag.name + " statistics"

@receiver(post_save, sender=User)
def create_statistics_user(sender, instance, created, **kwargs):
    if created:
        StatisticsTotal.objects.create(user=instance)

@receiver(post_save, sender=Tag)
def create_statistics_tag(sender, instance, created, **kwargs):
    if created:
        StatisticsTag.objects.create(tag=instance)
