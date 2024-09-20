from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = "api-v1"

urlpatterns = [
    # Registration
    path("registration/", views.RegistrationApiView.as_view(), name="registration"),
    # Activation
    path(
        "activation/confirm/<str:token>",
        views.ActivationApiView.as_view(),
        name="activation",
    ),
    # Resend activation
    path(
        "activation/resend/",
        views.ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
    # Change password
    path(
        "change-password", views.ChangePasswordApiView.as_view(), name="change-password"
    ),
    # Reset password
    path(
        "reset-password",
        views.RequestPasswordResetApiView.as_view(),
        name="reset-password",
    ),
    path(
        "reset-password/confirm/<str:token>",
        views.ResetPasswordApiView.as_view(),
        name="reset-password-confirm",
    ),
    # Login token
    path("token/login/", views.CustomAuthToken.as_view(), name="token-login"),
    path("token/logout/", views.CustomDiscardAuthToken.as_view(), name="token-logout"),
    # Login jwt
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
