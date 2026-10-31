
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from accounts.permissions import IsTeacherOrAdministrator
from .models import Student, Teacher, SchoolClass, Subject
from .serializers import (
    StudentSerializer,
    TeacherSerializer,
    SchoolClassSerializer,
    SubjectSerializer,
)


class SchoolReadOnlyForStudents(IsAuthenticated):
    """
    Students can view records.
    Teachers and administrators can manage records.
    """

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.role in ("TEACHER", "ADMIN")


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related("user").all()
    serializer_class = StudentSerializer
    permission_classes = [SchoolReadOnlyForStudents]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related("user").all()
    serializer_class = TeacherSerializer
    permission_classes = [SchoolReadOnlyForStudents]


class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [SchoolReadOnlyForStudents]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.prefetch_related("teachers").all()
    serializer_class = SubjectSerializer
    permission_classes = [SchoolReadOnlyForStudents]
