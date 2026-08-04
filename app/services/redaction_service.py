from app.services.detection_service import (
    detect_with_regex,
    detect_with_presidio,
    merge_entities,
)

from app.services.mapping_service import PlaceholderMapper


def redact_text(text: str):
    """
    Hybrid Redaction Engine
    Regex + Presidio + Dynamic Placeholder Mapping
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

    # Step 4 - Initialize mapper
    mapper = PlaceholderMapper()

    # Step 5 - Redact
    redacted_text = text

    # Longest values first (avoids partial replacement issues)
    entities = sorted(
        entities,
        key=lambda x: len(x.value),
        reverse=True,
    )

    for entity in entities:

        placeholder = mapper.get_placeholder(
            entity.type,
            entity.value,
        )

        redacted_text = redacted_text.replace(
            entity.value,
            placeholder,
        )

    return redacted_text, entities