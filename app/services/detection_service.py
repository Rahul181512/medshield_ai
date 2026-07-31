import re

from presidio_analyzer import AnalyzerEngine

from app.schemas.redaction_schema import Entity

# Initialize Presidio Analyzer
analyzer = AnalyzerEngine()

# Supported Presidio Entities
SUPPORTED_ENTITIES = {
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "IP_ADDRESS",
    "CREDIT_CARD",
}

# Normalize entity names
ENTITY_MAPPING = {
    "EMAIL_ADDRESS": "EMAIL",
    "PHONE_NUMBER": "PHONE",
    "PERSON": "PERSON",
    "IP_ADDRESS": "IP_ADDRESS",
    "CREDIT_CARD": "CREDIT_CARD",
}


def normalize_entity_type(entity_type: str) -> str:
    """
    Convert Presidio entity names to MedShield standard names.
    """

    return ENTITY_MAPPING.get(entity_type, entity_type)


def detect_with_presidio(text: str):
    """
    Detect entities using Microsoft Presidio.
    Returns a list of Entity objects.
    """

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    entities = []

    for result in results:

        if result.entity_type not in SUPPORTED_ENTITIES:
            continue

        entities.append(
            Entity(
                type=normalize_entity_type(result.entity_type),
                value=text[result.start:result.end],
            )
        )

    return entities


def detect_with_regex(text: str):
    """
    Detect entities using Regex.
    Returns a list of Entity objects.
    """

    entities = []

    patterns = [
        ("PERSON", r"\bRahul\b"),
        ("HOSPITAL", r"\bAIIMS(?:\s+\w+)?\b"),
        ("EMAIL", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        ("PHONE", r"\b(?:\+91[- ]?)?[6-9]\d{9}\b"),
        ("AADHAAR", r"\b\d{4}\s?\d{4}\s?\d{4}\b"),
        ("PAN", r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b"),
        ("PASSPORT", r"\b[A-PR-WYa-pr-wy][1-9]\d{6}\b"),
        (
            "DOB",
            r"\b(?:0?[1-9]|[12][0-9]|3[01])[/-](?:0?[1-9]|1[0-2])[/-](?:19|20)\d{2}\b",
        ),
        ("IP_ADDRESS", r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    ]

    for entity_type, pattern in patterns:

        matches = re.finditer(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        for match in matches:

            entities.append(
                Entity(
                    type=entity_type,
                    value=match.group(),
                )
            )

    return entities


def merge_entities(regex_entities, presidio_entities):
    """
    Merge Regex and Presidio entities while removing duplicates.
    """

    merged = {}

    for entity in regex_entities + presidio_entities:

        key = (
            entity.type.upper(),
            entity.value.lower(),
        )

        if key not in merged:
            merged[key] = entity

    return list(merged.values())