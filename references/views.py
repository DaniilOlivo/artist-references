from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from references.models import Reference

class IndexView(LoginRequiredMixin, TemplateView):
    extra_context = {"active_section": "index", "part": "main"}
    template_name ='references/index.html'

class ReferenceView(LoginRequiredMixin, ListView):
    extra_context = {"active_section": "references", "part": "main"}
    template_name ='references/list_refs.html'

    model = Reference
    context_object_name = "references"

    def get_queryset(self):
        return self.request.user.references
