from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view(next_page="accounts:user-login"), name="user-logout"),
    path("register/", views.CustomRegisterView.as_view(), name="user-register"),
    path("api/v1/", include("accounts.api.v1.urls")),
]
