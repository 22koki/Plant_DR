def analyze_scan(*, scan_type: str, image_name: str) -> dict:
    """
    Temporary deterministic diagnosis stub.

    The API contract is intentionally shaped like the future vision-AI
    response so we can build and test the full upload -> diagnosis flow now,
    then swap this implementation for a real provider without rewriting the UI.
    """
    labels = {
        "plant": ("Unknown plant", "Plant species undetermined"),
        "crop": ("Crop plant", "Species pending AI identification"),
        "flower": ("Flowering plant", "Species pending AI identification"),
        "lawn": ("Lawn / turf", "Grass species pending AI identification"),
        "tree": ("Tree / shrub", "Species pending AI identification"),
    }

    plant_name, scientific_name = labels.get(
        scan_type, ("Vegetation", "Species pending AI identification")
    )

    return {
        "plant_name": plant_name,
        "scientific_name": scientific_name,
        "likely_condition": "Analysis provider not connected",
        "confidence": "pending",
        "severity": "unknown",
        "symptoms": [
            "Image received successfully",
            "Image stored by backend",
            "Ready for vision analysis",
        ],
        "explanation": (
            f"The backend received {image_name}. "
            "The next milestone is connecting a vision-capable AI provider "
            "to identify the vegetation and visible symptoms."
        ),
        "alternative_conditions": [],
        "treatment": [],
        "prevention": [],
        "sources": [],
        "model_version": "stub-v1",
    }
