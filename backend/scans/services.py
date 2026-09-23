import base64
import json
import mimetypes

from django.conf import settings
from openai import OpenAI


class VisionConfigurationError(RuntimeError):
    pass


class VisionAnalysisError(RuntimeError):
    pass


SYSTEM_PROMPT = """You are the vision analysis layer for Plant Doctor AR, a plant-health decision-support application.
Analyze only evidence visible in the supplied image. Do not claim certainty that the image cannot support.
Identify the plant when reasonably possible, describe visible symptoms, and suggest plausible plant-health conditions.
Confidence must be one of: low, medium, high.
Severity must be one of: unknown, mild, moderate, severe.
Keep likely_condition concise. If the image is insufficient, say so explicitly.
Do not provide pesticide dosages, chemical mixing instructions, or unsupported treatment advice.
Return only valid JSON matching the requested schema."""


def _schema():
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "plant_name": {"type": "string"},
            "scientific_name": {"type": "string"},
            "likely_condition": {"type": "string"},
            "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
            "severity": {"type": "string", "enum": ["unknown", "mild", "moderate", "severe"]},
            "symptoms": {"type": "array", "items": {"type": "string"}, "maxItems": 8},
            "explanation": {"type": "string"},
            "alternative_conditions": {"type": "array", "items": {"type": "string"}, "maxItems": 5},
        },
        "required": [
            "plant_name", "scientific_name", "likely_condition", "confidence",
            "severity", "symptoms", "explanation", "alternative_conditions"
        ],
    }


def analyze_scan(*, scan_type: str, image_path: str, image_name: str) -> dict:
    if not settings.OPENAI_API_KEY:
        raise VisionConfigurationError(
            "OPENAI_API_KEY is not configured. Add it to backend/.env before running AI diagnosis."
        )

    with open(image_path, "rb") as image_file:
        raw = image_file.read()

    if len(raw) > settings.MAX_SCAN_IMAGE_BYTES:
        raise VisionAnalysisError("Image is too large for analysis.")

    mime_type = mimetypes.guess_type(image_name)[0] or "image/jpeg"
    if mime_type not in {"image/jpeg", "image/png", "image/webp", "image/gif"}:
        raise VisionAnalysisError("Unsupported image format.")

    data_url = f"data:{mime_type};base64,{base64.b64encode(raw).decode('ascii')}"
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        response = client.responses.create(
            model=settings.VISION_MODEL,
            input=[
                {"role": "system", "content": [{"type": "input_text", "text": SYSTEM_PROMPT}]},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                f"Scan type selected by user: {scan_type}. "
                                "Analyze this image for plant identity and visible plant-health symptoms."
                            ),
                        },
                        {"type": "input_image", "image_url": data_url},
                    ],
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "plant_diagnosis",
                    "strict": True,
                    "schema": _schema(),
                }
            },
        )
        result = json.loads(response.output_text)
    except Exception as exc:
        raise VisionAnalysisError("Vision analysis failed. Please try again.") from exc

    return {
        **result,
        "treatment": [],
        "prevention": [],
        "sources": [],
        "model_version": settings.VISION_MODEL,
    }
