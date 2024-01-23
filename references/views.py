from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.conf import settings
from django.core.paginator import Paginator
from references.models import Reference, Tag
from django.urls import reverse

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

class CreateReferenceView(LoginRequiredMixin, CreateView):
    model = Reference
    template_name = "references/create_reference.html"
    fields = ["title", "image", "tags"]

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('references')  
        return super().post(request, *args, **kwargs)

class UpdateReferenceView(LoginRequiredMixin, UpdateView):
    model = Reference
    template_name = "references/edit_reference.html"
    fields = ["title", "tags"]
    
    def get_success_url(self):
        return reverse("references")
    
class DeleteReferenceView(LoginRequiredMixin, DeleteView):
    model = Reference
    template_name = "references/delete_reference.html"

    def get_success_url(self):
        return reverse("references")

class ListTagsView(LoginRequiredMixin, ListView):
    extra_context = {"active_section": "tags", "part": "main"}
    model = Tag
    context_object_name = "tags"
    template_name = "references/list_tags.html"
    paginate_by = 6

    def get_queryset(self):
        return self.request.user.tags.all()

class CreateTagView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = "references/create_tag.html"
    fields = ["name"]

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('tags')  
        return super().post(request, *args, **kwargs)
    
class UpdateTagView(LoginRequiredMixin, UpdateView):
    model = Tag
    template_name = "references/edit_tag.html"
    fields = ["name"]

    def get_success_url(self):
        return reverse("tags")
