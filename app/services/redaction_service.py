import re

from app.schemas.redaction_schema import Entity


def redact_text(text: str):
    """
    Perform regex-based PHI/PII redaction.
    Returns:
        tuple: (redacted_text, entities)
    """

    redacted = text
    entities = []

    patterns = [
        # Demo Person
        ("PERSON", r"\bRahul\b", "[NAME_001]"),

        # Hospital
        ("HOSPITAL", r"\bAIIMS(?:\s+\w+)?\b", "[HOSPITAL_001]"),

        # Email
        (
            "EMAIL",
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            "[EMAIL_001]",
        ),

        # Phone Number
        (
            "PHONE",
            r"\b(?:\+91[- ]?)?[6-9]\d{9}\b",
            "[PHONE_001]",
        ),

        # Aadhaar
        (
            "AADHAAR",
            r"\b\d{4}\s?\d{4}\s?\d{4}\b",
            "[AADHAAR_001]",
        ),

        # PAN Card
        (
            "PAN",
            r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
            "[PAN_001]",
        ),

        # Passport (Indian)
        (
            "PASSPORT",
            r"\b[A-PR-WYa-pr-wy][1-9]\d{6}\b",
            "[PASSPORT_001]",
        ),

        # Date of Birth
        (
            "DOB",
            r"\b(?:0?[1-9]|[12][0-9]|3[01])[/-](?:0?[1-9]|1[0-2])[/-](?:19|20)\d{2}\b",
            "[DOB_001]",
        ),

        # IPv4 Address
        (
            "IP_ADDRESS",
            r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            "[IP_001]",
        ),
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

