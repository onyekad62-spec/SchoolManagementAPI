
from rest_framework import serializers
from .models import Exam, StudentScore


def calculate_grade(percentage):
    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 45:
        return "D"
    elif percentage >= 40:
        return "E"
    return "F"


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
    percentage = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()

    class Meta:
        model = StudentScore
        fields = [
            "id",
            "exam",
            "exam_name",
            "student",
            "student_name",
            "marks_obtained",
            "percentage",
            "grade",
            "remarks",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_percentage(self, obj):
        if not obj.exam.total_marks:
            return 0
        return round(
            float(obj.marks_obtained) / obj.exam.total_marks * 100,
            2
        )

    def get_grade(self, obj):
        return calculate_grade(self.get_percentage(obj))

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
