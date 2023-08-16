from django.urls import path

from user import views

urlpatterns = [
    path("create_user/", views.UserRegistration.as_view(), name="create"),
    path("login_user/", views.UserLogin.as_view(), name="login"),
    path("user_register/", views.JinjaRegistration.as_view(), name="register"),
    path("user_login/", views.JinjaLogin.as_view(), name="login"),
    path("index/", views.home_page, name="index"),
    path("user_logout/", views.user_logout, name="logout")
]
