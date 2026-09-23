from django.db import models

class PlantScan(models.Model):
    class ScanType(models.TextChoices):
        PLANT = "plant", "Plant"
        CROP = "crop", "Crop"
        FLOWER = "flower", "Flower"
        LAWN = "lawn", "Lawn / Grass"
        TREE = "tree", "Tree / Shrub"

    image = models.ImageField(upload_to="scans/%Y/%m/%d/")
    scan_type = models.CharField(max_length=20, choices=ScanType.choices)
    plant_name = models.CharField(max_length=120, blank=True)
    scientific_name = models.CharField(max_length=160, blank=True)
    likely_condition = models.CharField(max_length=180, blank=True)
    confidence = models.CharField(max_length=20, blank=True)
    severity = models.CharField(max_length=20, blank=True)
    symptoms = models.JSONField(default=list, blank=True)
    explanation = models.TextField(blank=True)
    alternative_conditions = models.JSONField(default=list, blank=True)
    treatment = models.JSONField(default=list, blank=True)
    prevention = models.JSONField(default=list, blank=True)
    sources = models.JSONField(default=list, blank=True)
    model_version = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_scan_type_display()} scan #{self.pk}"
