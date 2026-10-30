from django.db import models
from school.models import Student, SchoolClass


class SchoolFee(models.Model):
    name = models.CharField(max_length=100)
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="school_fees"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    academic_year = models.CharField(max_length=20)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.school_class.name}"


class FeePayment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="fee_payments"
    )
    school_fee = models.ForeignKey(
        SchoolFee,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    payment_reference = models.CharField(
        max_length=100,
        unique=True
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.school_fee.name} - {self.status}"