from django.views.generic import TemplateView

class IndexView(TemplateView):
    extra_context = {"active_section": "index"}
    template_name ='references/index.html'
