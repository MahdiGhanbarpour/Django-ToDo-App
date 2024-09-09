from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view(next_page="accounts:user-login"), name="user-logout"),
    path("register/", views.CustomRegisterView.as_view(), name="user-register")
]
