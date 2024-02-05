from django.views.generic import TemplateView
from references.models import Reference
from statistic.models import StatisticsTag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Count

def create_stat_block(attempts, refs):
    def create_stat(label, value):
        return {
            "label": label,
            "value": value,
        }

    stat = {
        "attempts": create_stat("Total attempts", attempts),
        "images": create_stat("Images", refs.count()),
    }

    statuses = ["new", "fail", "error", "success", "masterpiece"]
    stats_statuses = {}
    for status in statuses:
        stats_statuses[status] = create_stat(
            status.title(),
            refs.filter(status=status).count()
        )
    stat.update(stats_statuses)
    
    return stat

class StatisticsPage (LoginRequiredMixin, TemplateView):
    template_name = "statistic/statistics.html"
    extra_context = {
        "active_section": "statistics",
        "part": "main",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        refs = user.references.all()
        context["total"] = create_stat_block(
            user.statistics.attempts,
            refs
        )

        tags = self.request.user.tags.all()
        context["tags"] = []
        for tag in tags:
            stat = create_stat_block(
                tag.statistics.attempts,
                tag.references.all()
            )
            stat["id"] = tag.id
            context["tags"].append(stat)

        return context
    
def statistics_tags_api(request):
    tags = request.user.tags.all().annotate(ref_count=Count("references"))

    return JsonResponse(list(tags.values()), safe=False)
    