from rest_framework import serializers

from .models import Student, Teacher, SchoolClass, Subject


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "username",
            "admission_number",
            "date_of_birth",
            "address",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Teacher
        fields = [
            "id",
            "user",
            "username",
            "employee_number",
            "department",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class SchoolClassSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Student.objects.all(),
        required=False,
    )

    class Meta:
        model = SchoolClass
        fields = [
            "id",
            "name",
            "level",
            "academic_year",
            "students",
        ]
        read_only_fields = ["id"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"