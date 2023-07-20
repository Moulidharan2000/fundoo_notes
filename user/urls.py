from django.urls import path

from user import views

urlpatterns = [
    path("create_user/", views.UserRegistration.as_view(), name="create"),
    path("login_user/", views.UserLogin.as_view(), name="login"),
]
