from django.conf import settings
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    admission_number = models.CharField(max_length=30, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admission_number} - {self.user.username}"


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )
    employee_number = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_number} - {self.user.username}"
    

class SchoolClass(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    teachers = models.ManyToManyField(
        Teacher,
        blank=True,
        related_name="subjects",
    )

    def __str__(self):
        return self.name

