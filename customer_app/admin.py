from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "phone_number",
        "is_verified",
        "is_active",
        "created_at",
    )
    search_fields = ("username", "email", "phone_number")
    list_filter = ("is_verified", "is_active", "created_at", "updated_at")
    ordering = ("-created_at",)
