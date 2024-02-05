from django.views.generic import TemplateView
from statistic.models import StatisticsTag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Count

class StatisticsPage (LoginRequiredMixin, TemplateView):
    template_name = "statistic/statistics.html"
    extra_context = {
        "active_section": "statistics",
        "part": "main",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = self.request.user.statistics
        tags = self.request.user.tags.all()
        context["tags"] = StatisticsTag.objects.filter(tag__in=tags)
        return context
    
def statistics_tags_api(request):
    tags = request.user.tags.all().annotate(ref_count=Count("references"))

    return JsonResponse(list(tags.values()), safe=False)
    