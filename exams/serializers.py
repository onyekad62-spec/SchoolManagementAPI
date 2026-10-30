from rest_framework import serializers
from .models import Exam, StudentScore


class ExamSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(
        source="subject.name",
        read_only=True
    )
    class_name = serializers.CharField(
        source="school_class.name",
        read_only=True
    )

    class Meta:
        model = Exam
        fields = [
            "id",
            "name",
            "school_class",
            "class_name",
            "subject",
            "subject_name",
            "exam_date",
            "total_marks",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class StudentScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.user.username",
        read_only=True
    )
    exam_name = serializers.CharField(
        source="exam.name",
        read_only=True
    )

    class Meta:
        model = StudentScore
        fields = [
            "id",
            "exam",
            "exam_name",
            "student",
            "student_name",
            "marks_obtained",
            "remarks",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        exam = attrs.get("exam", getattr(self.instance, "exam", None))
        marks = attrs.get(
            "marks_obtained",
            getattr(self.instance, "marks_obtained", None)
        )

        if exam and marks is not None:
            if marks < 0 or marks > exam.total_marks:
                raise serializers.ValidationError({
                    "marks_obtained": (
                        f"Marks must be between 0 and {exam.total_marks}."
                    )
                })

        return attrs