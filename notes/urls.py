from django.urls import path
from notes import views

urlpatterns = [
    path("api/notes/", views.NotesAPI.as_view(), name="notes"),
]
