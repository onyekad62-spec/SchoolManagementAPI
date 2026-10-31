
from django.db.models import Sum, Count, Avg

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import Exam, StudentScore
from .serializers import (
    ExamSerializer,
    StudentScoreSerializer,
    calculate_grade,
)


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related(
        "school_class",
        "subject"
    ).all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def results(self, request, pk=None):
        exam = self.get_object()

        scores = StudentScore.objects.filter(
            exam=exam
        ).select_related("student", "student__user")

        results = []

        for score in scores:
            percentage = (
                float(score.marks_obtained) / exam.total_marks * 100
                if exam.total_marks else 0
            )

            results.append({
                "student_id": score.student.id,
                "student_name": score.student.user.username,
                "admission_number": score.student.admission_number,
                "marks_obtained": float(score.marks_obtained),
                "total_marks": exam.total_marks,
                "percentage": round(percentage, 2),
                "grade": calculate_grade(percentage),
            })

        return Response({
            "exam": exam.name,
            "school_class": exam.school_class.name,
            "subject": exam.subject.name,
            "number_of_students": len(results),
            "results": results,
        })


class StudentScoreViewSet(viewsets.ModelViewSet):
    queryset = StudentScore.objects.select_related(
        "exam",
        "student",
        "student__user"
    ).all()
    serializer_class = StudentScoreSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="class_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=True,
                description="ID of the school class"
            )
        ]
    )
    @action(detail=False, methods=["get"])
    def class_results(self, request):
        class_id = request.query_params.get("class_id")

        if not class_id:
            return Response(
                {"error": "Please provide class_id."},
                status=400
            )

        try:
            class_id = int(class_id)
        except (ValueError, TypeError):
            return Response(
                {"error": "class_id must be a valid number."},
                status=400
            )

        scores = self.get_queryset().filter(
            exam__school_class_id=class_id
        )

        results = []

        for student in scores.values(
            "student_id",
            "student__user__username",
            "student__admission_number",
        ).distinct():

            student_scores = scores.filter(
                student_id=student["student_id"]
            )

            totals = student_scores.aggregate(
                total=Sum("marks_obtained"),
                average=Avg("marks_obtained"),
                exams=Count("id"),
            )

            total_possible = sum(
                score.exam.total_marks
                for score in student_scores.select_related("exam")
            )

            percentage = (
                float(totals["total"]) / total_possible * 100
                if total_possible else 0
            )

            results.append({
                "student_id": student["student_id"],
                "student_name": student["student__user__username"],
                "admission_number": student["student__admission_number"],
                "exams_taken": totals["exams"],
                "total_marks_obtained": float(totals["total"] or 0),
                "average_marks": round(float(totals["average"] or 0), 2),
                "percentage": round(percentage, 2),
                "grade": calculate_grade(percentage),
            })

        return Response({
            "class_id": class_id,
            "number_of_students": len(results),
            "results": results,
        })
