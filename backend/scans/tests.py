import shutil
import tempfile
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase

from .models import PlantScan
from .services import VisionAnalysisError, VisionConfigurationError


TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ScanApiTests(APITestCase):
    def tearDown(self):
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def image(self):
        return SimpleUploadedFile(
            "leaf.jpg",
            b"fake-jpeg-for-mocked-analysis",
            content_type="image/jpeg",
        )

    def test_health_endpoint(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "ok")

    @patch("scans.views.analyze_scan")
    def test_scan_upload_returns_structured_diagnosis(self, analyze):
        analyze.return_value = {
            "plant_name": "Tomato",
            "scientific_name": "Solanum lycopersicum",
            "likely_condition": "Early blight",
            "confidence": "high",
            "severity": "moderate",
            "symptoms": ["Brown concentric leaf lesions", "Yellowing"],
            "explanation": "Visible lesions are consistent with early blight.",
            "alternative_conditions": ["Septoria leaf spot"],
            "treatment": [],
            "prevention": [],
            "sources": [],
            "model_version": "test-model",
        }

        response = self.client.post(
            "/api/scans/analyze/",
            {"scan_type": "crop", "image": self.image()},
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["plant_name"], "Tomato")
        self.assertEqual(response.data["likely_condition"], "Early blight")
        self.assertEqual(response.data["confidence"], "high")
        self.assertEqual(PlantScan.objects.count(), 1)

    @patch("scans.views.analyze_scan")
    def test_configuration_failure_does_not_keep_scan(self, analyze):
        analyze.side_effect = VisionConfigurationError("Missing API key")
        response = self.client.post(
            "/api/scans/analyze/",
            {"scan_type": "plant", "image": self.image()},
            format="multipart",
        )
        self.assertEqual(response.status_code, 503)
        self.assertEqual(PlantScan.objects.count(), 0)

    @patch("scans.views.analyze_scan")
    def test_provider_failure_does_not_keep_scan(self, analyze):
        analyze.side_effect = VisionAnalysisError("Vision analysis failed")
        response = self.client.post(
            "/api/scans/analyze/",
            {"scan_type": "plant", "image": self.image()},
            format="multipart",
        )
        self.assertEqual(response.status_code, 502)
        self.assertEqual(PlantScan.objects.count(), 0)

    def test_invalid_scan_type_is_rejected(self):
        response = self.client.post(
            "/api/scans/analyze/",
            {"scan_type": "spaceship", "image": self.image()},
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)
