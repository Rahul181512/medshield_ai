from app.services.detection_service import (
    detect_with_regex,
    detect_with_presidio,
    merge_entities,
)

from app.services.mapping_service import PlaceholderMapper


def redact_text(
    text: str,
    session_id: str,
):
    """
    Hybrid Redaction Engine

    Regex + Presidio + Redis-backed Dynamic Placeholder Mapping
    """

    # Step 1 - Regex Detection
    regex_entities = detect_with_regex(text)

    # Step 2 - Presidio Detection
    presidio_entities = detect_with_presidio(text)

    # Step 3 - Merge detections
    entities = merge_entities(
        regex_entities,
        presidio_entities,
    )

    # Step 4 - Redis-backed mapper
    mapper = PlaceholderMapper(
        session_id=session_id,
    )

    # Step 5 - Redact
    redacted_text = text

    # Longest values first
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