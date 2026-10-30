from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Exam, StudentScore
from .serializers import ExamSerializer, StudentScoreSerializer


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related(
        "school_class",
        "subject"
    ).all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]


class StudentScoreViewSet(viewsets.ModelViewSet):
    queryset = StudentScore.objects.select_related(
        "exam",
        "student",
        "student__user"
    ).all()
    serializer_class = StudentScoreSerializer
    permission_classes = [IsAuthenticated]