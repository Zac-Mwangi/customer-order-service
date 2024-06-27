from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *  # Adjust the import path as needed

# Register your models here.
@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    list_display = ("id", "customer", "item", "amount", "time")
    search_fields = ("item", "customer__name")
    list_filter = ("time", "amount")
