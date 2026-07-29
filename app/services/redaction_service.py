import re

from app.schemas.redaction_schema import Entity


def redact_text(text: str):
    """
    Perform basic regex-based PHI/PII redaction.
    Returns:
        tuple: (redacted_text, entities)
    """

    redacted = text
    entities = []

    patterns = [
        ("PERSON", r"\bRahul\b", "[NAME_001]"),
        ("HOSPITAL", r"\bAIIMS(?:\s+\w+)?\b", "[HOSPITAL_001]"),
        ("EMAIL", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[EMAIL_001]"),
        ("PHONE", r"\b\d{10}\b", "[PHONE_001]"),
        ("AADHAAR", r"\b\d{4}\s?\d{4}\s?\d{4}\b", "[AADHAAR_001]"),
    ]

    for entity_type, pattern, replacement in patterns:

        matches = re.findall(pattern, redacted, flags=re.IGNORECASE)

        for match in matches:
            entities.append(
                Entity(
                    type=entity_type,
                    value=match,
                )
            )

        redacted = re.sub(
            pattern,
            replacement,
            redacted,
            flags=re.IGNORECASE,
        )

    return redacted, entities