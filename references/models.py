from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
import json

priority_map = None
with open(settings.BASE_DIR / "references" / "config" / "priority_map.json") as f:
    priority_map = json.load(f)

def get_titles_statuses():
    statusesArr = priority_map["priority"].keys()
    return " ".join(statusesArr)

def get_image_path(instance, filename):
    return 'uploads/{0}/{1}'.format(instance.user.id, filename)

class Tag (models.Model):
    name = models.CharField(
        max_length=120)
    priority = models.FloatField(default=priority_map['base'])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name

class Reference (models.Model):
    Statuses = models.TextChoices("Status", get_titles_statuses())

    title = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='references')
    image = models.ImageField(upload_to=get_image_path)
    tags = models.ManyToManyField(Tag, related_name='references')
    status = models.CharField(max_length=100, choices=Statuses.choices, default=Statuses.new)

    image_card = ImageSpecField(source='image',
                                    processors=[ResizeToFit(170, 170, mat_color="white")],
                                    format="JPEG")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.image.name
        super().save(*args, **kwargs)