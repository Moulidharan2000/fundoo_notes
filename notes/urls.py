from django.urls import path
from notes import views

urlpatterns = [
    path("api/notes/", views.NotesAPI.as_view(), name="notes"),
    path("api/labels/", views.LabelAPI.as_view(), name="labels"),
    path("api/archived/", views.IsArchiveTrash.as_view({'get': 'list', 'post': 'create'}), name="archived"),
    path("api/trash/", views.IsArchiveTrash.as_view({'get': 'get_trash', 'post': 'set_trash'}), name="trash")
]
