from rest_framework import serializers
from .models import PlantScan

class PlantScanSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PlantScan
        fields = [
            "id",
            "image",
            "image_url",
            "scan_type",
            "plant_name",
            "scientific_name",
            "likely_condition",
            "confidence",
            "severity",
            "symptoms",
            "explanation",
            "alternative_conditions",
            "treatment",
            "prevention",
            "sources",
            "model_version",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "plant_name",
            "scientific_name",
            "likely_condition",
            "confidence",
            "severity",
            "symptoms",
            "explanation",
            "alternative_conditions",
            "treatment",
            "prevention",
            "sources",
            "model_version",
            "created_at",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if not obj.image:
            return None
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url
