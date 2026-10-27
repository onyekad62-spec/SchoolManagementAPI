from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Student, Teacher
from .serializers import StudentSerializer, TeacherSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related("user").all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related("user").all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
