from django.db.models import Sum

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from school.models import Student
from .models import SchoolFee, FeePayment
from .serializers import SchoolFeeSerializer, FeePaymentSerializer


class FeeManagementPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.role in ("TEACHER", "ADMIN")


class SchoolFeeViewSet(viewsets.ModelViewSet):
    queryset = SchoolFee.objects.select_related(
        "school_class"
    ).all()
    serializer_class = SchoolFeeSerializer
    permission_classes = [FeeManagementPermission]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="student_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Student profile ID"
            )
        ]
    )
    @action(detail=False, methods=["get"])
    def outstanding(self, request):
        student_id = request.query_params.get("student_id")

        if not student_id:
            return Response(
                {"error": "Please provide student_id."},
                status=400
            )

        try:
            student = Student.objects.get(id=int(student_id))
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid student_id."},
                status=400
            )
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found."},
                status=404
            )

        fees = SchoolFee.objects.filter(
            school_class__students=student
        ).select_related("school_class")

        results = []

        for fee in fees:
            paid = FeePayment.objects.filter(
                student=student,
                school_fee=fee,
                status=FeePayment.Status.PAID
            ).aggregate(total=Sum("amount_paid"))["total"] or 0

            balance = max(fee.amount - paid, 0)

            results.append({
                "fee_id": fee.id,
                "fee_name": fee.name,
                "term": fee.term,
                "academic_year": fee.academic_year,
                "amount_due": fee.amount,
                "total_paid": paid,
                "outstanding_balance": balance,
                "due_date": fee.due_date,
            })

        return Response({
            "student_id": student.id,
            "number_of_fees": len(results),
            "total_outstanding": sum(
                (item["outstanding_balance"] for item in results),
                start=0
            ),
            "fees": results,
        })


class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.select_related(
        "student",
        "student__user",
        "school_fee",
    ).all()
    serializer_class = FeePaymentSerializer
    permission_classes = [FeeManagementPermission]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="student_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Student profile ID"
            )
        ]
    )
    @action(detail=False, methods=["get"])
    def history(self, request):
        student_id = request.query_params.get("student_id")

        if not student_id:
            return Response(
                {"error": "Please provide student_id."},
                status=400
            )

        try:
            student_id = int(student_id)
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid student_id."},
                status=400
            )

        payments = self.get_queryset().filter(
            student_id=student_id
        ).order_by("-created_at")

        return Response({
            "student_id": student_id,
            "number_of_payments": payments.count(),
            "payments": FeePaymentSerializer(
                payments,
                many=True
            ).data,
        })