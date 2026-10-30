from rest_framework.routers import DefaultRouter
from .views import SchoolFeeViewSet, FeePaymentViewSet

router = DefaultRouter()
router.register("school-fees", SchoolFeeViewSet, basename="school-fee")
router.register("payments", FeePaymentViewSet, basename="fee-payment")

urlpatterns = router.urls