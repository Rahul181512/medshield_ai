

from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.redact import router as redact_router
from app.api.routes.audit import router as audit_router
from app.api.routes.users import router as users_router



app = FastAPI(
    title="MedShield AI",
    description="AI-powered PHI/PII Redaction Pipeline for Secure Healthcare LLM Integration",
    version="1.0.0"
)
app.include_router(auth_router)
app.include_router(redact_router)
app.include_router(audit_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to MedShield AI"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MedShield AI",
        "version": "1.0.0"
    }

@app.get("/version", tags=["System"])
def version():
    """
    Return application version information.
    """

    return {
        "application": "MedShield AI",
        "version": "1.0.0",
        "status": "stable",
    }