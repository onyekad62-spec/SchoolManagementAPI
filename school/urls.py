from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet,
    TeacherViewSet,
    SchoolClassViewSet,
    SubjectViewSet,
)

router = DefaultRouter()
router.register("students", StudentViewSet, basename="student")
router.register("teachers", TeacherViewSet, basename="teacher")
router.register("classes", SchoolClassViewSet, basename="school-class")
router.register("subjects", SubjectViewSet, basename="subject")

urlpatterns = router.urls