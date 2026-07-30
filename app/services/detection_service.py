from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()

SUPPORTED_ENTITIES = {
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "IP_ADDRESS",
    "CREDIT_CARD",
}


def detect_entities(text: str):
    """
    Detect supported PII entities using Microsoft Presidio.
    Only returns entities that MedShield AI supports.
    """

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    filtered_results = [
        result
        for result in results
        if result.entity_type in SUPPORTED_ENTITIES
    ]

    return filtered_results