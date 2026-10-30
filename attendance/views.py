
from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related(
        "student",
        "student__user",
    ).all()

    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        date = self.request.query_params.get("date")
        class_id = self.request.query_params.get("class_id")
        student_id = self.request.query_params.get("student_id")

        if date:
            queryset = queryset.filter(date=date)

        if class_id:
            queryset = queryset.filter(
                student__enrolled_classes__id=class_id
            )

        if student_id:
            queryset = queryset.filter(student_id=student_id)

        return queryset.distinct()

    @action(detail=False, methods=["get"])
    def summary(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        totals = queryset.aggregate(
            total=Count("id"),
            present=Count(
                "id",
                filter=Q(status=Attendance.Status.PRESENT),
            ),
            absent=Count(
                "id",
                filter=Q(status=Attendance.Status.ABSENT),
            ),
            late=Count(
                "id",
                filter=Q(status=Attendance.Status.LATE),
            ),
        )

        total = totals["total"]
        attended = totals["present"] + totals["late"]

        percentage = (
            round((attended / total) * 100, 2)
            if total else 0
        )

        return Response({
            "total_records": total,
            "present": totals["present"],
            "absent": totals["absent"],
            "late": totals["late"],
            "attended": attended,
            "attendance_percentage": percentage,
        })
