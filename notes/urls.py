from django.urls import path
from notes import views

urlpatterns = [
    path("api/notes/", views.NotesAPI.as_view(), name="notes"),
    path("api/labels/", views.LabelAPI.as_view(), name="labels"),
]
