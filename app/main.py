

from fastapi import FastAPI

app = FastAPI(
    title="MedShield AI",
    description="AI-powered PHI/PII Redaction Pipeline for Secure Healthcare LLM Integration",
    version="1.0.0"
)


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
