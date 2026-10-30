from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Django administration
    path("admin/", admin.site.urls),

    # Authentication endpoints
    path("api/accounts/", include("accounts.urls")),

    # Student and teacher endpoints
    path("api/school/", include("school.urls")),

    # API schema and interactive documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    path("api/attendance/", include("attendance.urls")),

    path("api/exams/", include("exams.urls")),
]
