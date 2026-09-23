from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PlantScan
from .serializers import PlantScanSerializer
from .services import VisionAnalysisError, VisionConfigurationError, analyze_scan


class ScanCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = PlantScanSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        scan = serializer.save()

        try:
            result = analyze_scan(
                scan_type=scan.scan_type,
                image_path=scan.image.path,
                image_name=scan.image.name,
            )
        except VisionConfigurationError as exc:
            scan.delete()
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except VisionAnalysisError as exc:
            scan.delete()
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        for field, value in result.items():
            setattr(scan, field, value)
        scan.save(update_fields=list(result.keys()))

        output = PlantScanSerializer(scan, context={"request": request})
        return Response(output.data, status=status.HTTP_201_CREATED)


class ScanListView(APIView):
    def get(self, request):
        scans = PlantScan.objects.all()[:20]
        serializer = PlantScanSerializer(scans, many=True, context={"request": request})
        return Response(serializer.data)


class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "Plant Doctor AR API"})
