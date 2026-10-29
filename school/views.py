from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Student, Teacher, SchoolClass, Subject
from .serializers import (
    StudentSerializer,
    TeacherSerializer,
    SchoolClassSerializer,
    SubjectSerializer,
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related("user").all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related("user").all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]


class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.prefetch_related("teachers").all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]