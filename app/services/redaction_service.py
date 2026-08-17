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

    regex_entities = detect_with_regex(text)

    presidio_entities = detect_with_presidio(text)

    entities = merge_entities(
        regex_entities,
        presidio_entities,
    )

    mapper = PlaceholderMapper(
        session_id=session_id,
    )

    redacted_text = text

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


def restore_text(
    text: str,
    session_id: str,
):
    """
    Restore placeholders using the session-based Redis mapping.
    """

    mapper = PlaceholderMapper(
        session_id=session_id,
    )

    restored_text = text

    mappings = mapper.get_all_mappings()

    for placeholder, original_value in mappings.items():
        restored_text = restored_text.replace(
            placeholder,
            original_value,
        )

    return restored_text