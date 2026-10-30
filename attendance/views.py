from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related(
        "student",
        "student__user",
    ).all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]