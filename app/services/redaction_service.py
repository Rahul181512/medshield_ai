from app.services.detection_service import (
    detect_with_regex,
    detect_with_presidio,
    merge_entities,
)


PLACEHOLDERS = {
    "PERSON": "[NAME_001]",
    "HOSPITAL": "[HOSPITAL_001]",
    "EMAIL": "[EMAIL_001]",
    "PHONE": "[PHONE_001]",
    "AADHAAR": "[AADHAAR_001]",
    "PAN": "[PAN_001]",
    "PASSPORT": "[PASSPORT_001]",
    "DOB": "[DOB_001]",
    "IP_ADDRESS": "[IP_001]",
    "CREDIT_CARD": "[CREDIT_CARD_001]",
}


def redact_text(text: str):
    """
    Hybrid Redaction Engine
    Regex + Presidio
    """

    # Step 1 - Detect using Regex
    regex_entities = detect_with_regex(text)

    # Step 2 - Detect using Presidio
    presidio_entities = detect_with_presidio(text)

    # Step 3 - Merge detections
    entities = merge_entities(
        regex_entities,
        presidio_entities,
    )

    # Step 4 - Redact
    redacted_text = text

    # Longest values first (avoids partial replacement issues)
    entities = sorted(
        entities,
        key=lambda x: len(x.value),
        reverse=True,
    )

    for entity in entities:

        placeholder = PLACEHOLDERS.get(
            entity.type,
            "[REDACTED]",
        )

        redacted_text = redacted_text.replace(
            entity.value,
            placeholder,
        )

    return redacted_text, entities