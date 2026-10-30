from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, StudentScoreViewSet

router = DefaultRouter()
router.register("exams", ExamViewSet, basename="exam")
router.register("scores", StudentScoreViewSet, basename="student-score")

urlpatterns = router.urls