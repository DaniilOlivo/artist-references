from django.views.generic import TemplateView
from statistic.models import StatisticsTotal, StatisticsTag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

class StatisticsPage (LoginRequiredMixin, TemplateView):
    template_name = "statistic/statistics.html"
    extra_context = {
        "active_section": "statistics",
        "part": "main",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = self.request.user.statistics
        return context
    
def statistics_tags_api(request):
    tags_user = request.user.tags.all()
    tags = StatisticsTag.objects.filter(tag__in=tags_user)
    return JsonResponse(list(tags), safe=False)

