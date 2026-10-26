from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    CurrentUserView,
    AdministratorTestView,
)


urlpatterns = [
    # Register a new student
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    # Log in and obtain JWT tokens
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    # Refresh an access token
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # Get the currently authenticated user's details
    path(
        "me/",
        CurrentUserView.as_view(),
        name="current_user",
    ),

    # Test administrator-only access
    path(
        "admin-test/",
        AdministratorTestView.as_view(),
        name="administrator_test",
    ),
]
