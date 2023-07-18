from django.urls import path

from user import views

urlpatterns = [
    path("create_user/", views.create_user, name="create"),
    path("login_user/", views.login_user, name="login"),
]
