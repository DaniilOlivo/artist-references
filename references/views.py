from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.conf import settings
from django.core.paginator import Paginator

class IndexView(LoginRequiredMixin, TemplateView):
    extra_context = {"active_section": "index", "part": "main"}
    template_name ='references/index.html'

def reference_list(request: HttpRequest):
    if not request.user.is_authenticated:
        redirect(settings.LOGIN_URL)
    list_objects = request.user.references.all()
    if request.method == 'POST':
        keyword = request.POST.get("search", False)
        if keyword:
            tags = request.user.tags.all()
            tags = tags.filter(name__icontains=keyword)
            list_objects = list_objects.filter(title__icontains=keyword) | list_objects.filter(tags__in=tags)

    paginator = Paginator(list_objects, 6)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "active_section": "references",
        "part": "main",
        "references": page_obj,
    }
    return render(request,'references/list_refs.html', context=context)
