from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.core.paginator import Paginator
from references.models import Reference, Tag
from django.urls import reverse
from references.core import get_ref, get_priority_map

def index_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    context = {
        "active_section": "index",
        "part": "main",
        "tags": request.user.tags.all()
    }

    if request.method == "POST":
        mode = request.POST.get("mode", "standard")
        tags = list(map(int, request.POST.getlist("tags", [])))
        request.session["selected_tags"] = tags
        return redirect(reverse("nature", kwargs={"mode": mode}))

    return render(request,'references/index.html', context)

class NotFoundRefsView (TemplateView):
    template_name = "references/warning.html"
    extra_context = {
        "part": "main",
        "message": "There are no references in this category"
    }

def nature(request, mode: str):
    tags = request.session.get("selected_tags", None)
    if tags:
        all_refs = request.user.references.filter(tags__in=tags)
    else:
        all_refs = request.user.references.all()

    selection_refs = all_refs
    if mode == "errors":
        selection_refs = all_refs.filter(status="error") | all_refs.filter(status="fail")
    elif mode == "improvement":
        selection_refs = all_refs.filter(status="success")
    elif mode == "news":
        selection_refs = all_refs.filter(status="new")
    
    ref_id = get_ref(selection_refs)

    if not ref_id:
        return redirect(reverse("not_refs"))

    ref = Reference.objects.get(id=ref_id)
    context = {
        "reference": ref,
        "mode": mode,
    }

    return render(request, "references/nature.html", context)

def skip_reference(request: HttpRequest, mode: str):
    if request.method == "POST":
        return redirect(reverse("nature", kwargs={'mode': mode}))

def update_weight_reference(request, mode, status, pk):
    obj = Reference.objects.get(id=pk)
    obj.status = status
    obj.save()

    deltas_map = get_priority_map()["tag_delta"]
    for tag in obj.tags.all():
        tag.priority += deltas_map[status]
        tag.save()

    if request.method == "POST":
        return redirect(reverse("nature", kwargs={'mode': mode}))
    
def dowland(request, pk):
    ref = Reference.objects.get(id=pk)
    print(ref.image.name)
    with ref.image.open("rb") as f:
        res = HttpResponse(f.read(), content_type="image/jpeg")
        res['Content-Disposition'] = 'attachment; filename="{}"'.format(ref.image.name)
        return res

def reference_list(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
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
    return render(request,'references/ref/list_refs.html', context=context)

class CreateReferenceView(LoginRequiredMixin, CreateView):
    model = Reference
    template_name = "references/ref/create_reference.html"
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
    template_name = "references/ref/edit_reference.html"
    fields = ["title", "tags"]
    
    def get_success_url(self):
        return reverse("references")
    
class DeleteReferenceView(LoginRequiredMixin, DeleteView):
    model = Reference
    template_name = "references/ref/delete_reference.html"

    def get_success_url(self):
        return reverse("references")

class ListTagsView(LoginRequiredMixin, ListView):
    extra_context = {"active_section": "tags", "part": "main"}
    model = Tag
    context_object_name = "tags"
    template_name = "references/tags/list_tags.html"
    paginate_by = 6

    def get_queryset(self):
        return self.request.user.tags.all()

class CreateTagView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = "references/tags/create_tag.html"
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
    template_name = "references/tags/edit_tag.html"
    fields = ["name"]

    def get_success_url(self):
        return reverse("tags")

class DeleteTagView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = "references/tags/delete_tag.html"
    
    def get_success_url(self):
        return reverse("tags")
