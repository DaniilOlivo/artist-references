from django.urls import path
from references.views import *

urlpatterns = [
    path("references/create/", CreateReferenceView.as_view(), name="create_reference"),
    path("references/edit/<int:pk>/", UpdateReferenceView.as_view(), name="edit_reference"),
    path("references/delete/<int:pk>/", DeleteReferenceView.as_view(), name="delete_reference"),
    path("references/list/", reference_list, name="references"),
    path("tags/list", ListTagsView.as_view(), name="tags"),
    path("tags/create/", CreateTagView.as_view(), name="create_tag"),
    path("tags/edit/<int:pk>/", UpdateTagView.as_view(), name="edit_tag"),
    path("tags/delete/<int:pk>/", DeleteTagView.as_view(), name="delete_tag"),
    path("", IndexView.as_view(), name="index"),
]

