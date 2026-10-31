
from django.db.models import Sum
from rest_framework import serializers

from .models import SchoolFee, FeePayment


class SchoolFeeSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(
        source="school_class.name",
        read_only=True
    )

    class Meta:
        model = SchoolFee
        fields = [
            "id",
            "name",
            "school_class",
            "class_name",
            "amount",
            "academic_year",
            "term",
            "due_date",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "The fee amount must be greater than zero."
            )
        return value


class FeePaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.user.username",
        read_only=True
    )
    fee_name = serializers.CharField(
        source="school_fee.name",
        read_only=True
    )
    total_paid = serializers.SerializerMethodField()
    outstanding_balance = serializers.SerializerMethodField()

    class Meta:
        model = FeePayment
        fields = [
            "id",
            "student",
            "student_name",
            "school_fee",
            "fee_name",
            "amount_paid",
            "payment_reference",
            "status",
            "payment_date",
            "total_paid",
            "outstanding_balance",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_total_paid(self, obj):
        total = FeePayment.objects.filter(
            student=obj.student,
            school_fee=obj.school_fee,
            status=FeePayment.Status.PAID
        ).aggregate(total=Sum("amount_paid"))["total"]
        return total or 0

    def get_outstanding_balance(self, obj):
        total_paid = self.get_total_paid(obj)
        balance = obj.school_fee.amount - total_paid
        return max(balance, 0)

    def validate_amount_paid(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Payment amount must be greater than zero."
            )
        return value
