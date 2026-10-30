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
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]