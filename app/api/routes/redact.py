from uuid import uuid4

from fastapi import APIRouter, Depends

from app.api.dependencies import require_role
from app.schemas.redaction_schema import (
    RedactionRequest,
    RedactionResponse,
)
from app.services.audit_service import log_redaction
from app.services.redaction_service import redact_text

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
    Redact PHI/PII using the hybrid detection engine
    with session-based Redis mapping.
    """

    # Generate a unique session for this request
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
        original_text=request.text,
        redacted_text=redacted_text,
        entities=entities,
    )


@router.post("/batch")
def batch_redact(
    texts: list[str],
):
    """
    Redact multiple documents in a single request.
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
                "original_text": text,
                "redacted_text": redacted_text,
                "entities": entities,
            }
        )

    return {
        "total_documents": len(texts),
        "results": results,
    }