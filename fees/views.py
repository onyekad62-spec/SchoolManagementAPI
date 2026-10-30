from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import SchoolFee, FeePayment
from .serializers import SchoolFeeSerializer, FeePaymentSerializer


class SchoolFeeViewSet(viewsets.ModelViewSet):
    queryset = SchoolFee.objects.select_related("school_class").all()
    serializer_class = SchoolFeeSerializer
    permission_classes = [IsAuthenticated]


class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.select_related(
        "student",
        "student__user",
        "school_fee",
    ).all()
    serializer_class = FeePaymentSerializer
    permission_classes = [IsAuthenticated]