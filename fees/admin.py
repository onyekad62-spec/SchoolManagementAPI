from django.contrib import admin
from .models import SchoolFee, FeePayment


@admin.register(SchoolFee)
class SchoolFeeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "school_class",
        "amount",
        "academic_year",
        "due_date",
    )
    list_filter = ("academic_year", "school_class")
    search_fields = ("name", "school_class__name")


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "school_fee",
        "amount_paid",
        "status",
        "payment_reference",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "student__user__username",
        "payment_reference",
    )