from django.db import models
from school.models import SchoolClass, Subject


class Exam(models.Model):
    name = models.CharField(max_length=100)
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="exams"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="exams"
    )
    exam_date = models.DateField()
    total_marks = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject.name}"


class StudentScore(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="scores"
    )
    student = models.ForeignKey(
        "school.Student",
        on_delete=models.CASCADE,
        related_name="exam_scores"
    )
    marks_obtained = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    remarks = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["exam", "student"],
                name="unique_student_score_per_exam"
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.exam.name} - {self.marks_obtained}"