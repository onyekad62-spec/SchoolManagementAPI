from django.contrib import admin
from .models import Exam, StudentScore


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("name", "school_class", "subject", "exam_date", "total_marks")
    list_filter = ("exam_date", "school_class", "subject")
    search_fields = ("name", "subject__name", "school_class__name")


@admin.register(StudentScore)
class StudentScoreAdmin(admin.ModelAdmin):
    list_display = ("student", "exam", "marks_obtained", "created_at")
    list_filter = ("exam",)
    search_fields = ("student__user__username", "exam__name")