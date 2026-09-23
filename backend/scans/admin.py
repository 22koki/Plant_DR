from django.contrib import admin
from .models import PlantScan

@admin.register(PlantScan)
class PlantScanAdmin(admin.ModelAdmin):
    list_display = ("id", "scan_type", "plant_name", "likely_condition", "created_at")
    list_filter = ("scan_type", "confidence", "severity")
    search_fields = ("plant_name", "scientific_name", "likely_condition")
