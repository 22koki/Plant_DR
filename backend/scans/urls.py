from django.urls import path
from .views import HealthView, ScanCreateView, ScanListView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("scans/", ScanListView.as_view(), name="scan-list"),
    path("scans/analyze/", ScanCreateView.as_view(), name="scan-analyze"),
]
