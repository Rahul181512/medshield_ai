from fastapi import APIRouter

from app.schemas.redaction_schema import (
    RedactionRequest,
    RedactionResponse,
)
from app.services.redaction_service import redact_text

router = APIRouter(
    prefix="/redact",
    tags=["Redaction"],
)


@router.post("/", response_model=RedactionResponse)
def redact(request: RedactionRequest):
    """
    Demo PHI/PII redaction endpoint.
    """

    redacted_text, entities = redact_text(request.text)

    return RedactionResponse(
        original_text=request.text,
        redacted_text=redacted_text,
        entities=entities,
    )