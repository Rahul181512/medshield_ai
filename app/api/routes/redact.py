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
    Demo PHI/PII redaction endpoint.
    """

    redacted_text, entities = redact_text(request.text)

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
def batch_redact(texts: list[str]):
    """
    Redact multiple documents in a single request.
    """

    results = []

    for text in texts:

        redacted_text, entities = redact_text(text)

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