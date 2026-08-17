from uuid import uuid4

from fastapi import APIRouter, Depends

from app.api.dependencies import require_role
from app.schemas.redaction_schema import (
    RedactionRequest,
    RedactionResponse,
    RestoreRequest,
)
from app.services.audit_service import log_redaction
from app.services.redaction_service import (
    redact_text,
    restore_text,
)

router = APIRouter(
    prefix="/redact",
    tags=["Redaction"],
)


@router.post("/", response_model=RedactionResponse)
def redact(
    request: RedactionRequest,
    current_user=Depends(require_role("doctor")),
):
    """
    Redact PHI/PII using hybrid detection
    with session-based Redis mapping.
    """

    session_id = str(uuid4())

    redacted_text, entities = redact_text(
        request.text,
        session_id=session_id,
    )

    log_redaction(
        username=current_user["username"],
        entities=entities,
    )

    return RedactionResponse(
        session_id=session_id,
        original_text=request.text,
        redacted_text=redacted_text,
        entities=entities,
    )


@router.post("/restore")
def restore(
    request: RestoreRequest,
    current_user=Depends(require_role("doctor")),
):
    """
    Restore placeholders using the Redis mapping
    associated with the session.
    """

    restored_text = restore_text(
        text=request.text,
        session_id=request.session_id,
    )

    return {
        "session_id": request.session_id,
        "restored_text": restored_text,
    }


@router.post("/batch")
def batch_redact(
    texts: list[str],
):
    """
    Redact multiple documents.
    Each document gets its own isolated session.
    """

    results = []

    for text in texts:

        session_id = str(uuid4())

        redacted_text, entities = redact_text(
            text,
            session_id=session_id,
        )

        results.append(
            {
                "session_id": session_id,
                "original_text": text,
                "redacted_text": redacted_text,
                "entities": entities,
            }
        )

    return {
        "total_documents": len(texts),
        "results": results,
    }