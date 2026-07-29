# MedShield AI

An AI-powered PHI/PII Redaction Pipeline designed to protect sensitive healthcare data before it is sent to Large Language Models (LLMs).

---

# Project Overview

MedShield AI is a secure middleware service that detects and redacts sensitive healthcare information before it reaches an LLM.

The project focuses on protecting Personally Identifiable Information (PII) and Protected Health Information (PHI) while allowing healthcare organizations to safely integrate AI systems into their workflows.

The current implementation provides secure authentication, regex-based PHI detection, audit logging, and a modular architecture that can later be extended using Microsoft Presidio and spaCy.

---

# Features

## Implemented

- FastAPI REST API
- JWT Authentication
- Password Hashing (bcrypt)
- User Authentication
- Regex-based PHI/PII Detection
- PHI/PII Redaction Service
- Audit Logging
- Swagger API Documentation
- Modular Service Layer

---

## Planned

- Microsoft Presidio Integration
- spaCy Named Entity Recognition
- Redis Mapping Vault
- Reversible Pseudonymization
- Streamlit Dashboard
- Docker Support
- Unit Testing
- CI/CD Pipeline

---

# Tech Stack

### Backend

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic

### Security

- JWT (python-jose)
- bcrypt

### AI / NLP (Upcoming)

- Microsoft Presidio
- spaCy

---

# Project Structure

```text
medshield_ai/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   └── redact.py
│   │   ├── __init__.py
│   │   └── dependencies.py
│   │
│   ├── auth/
│   │   ├── auth_handler.py
│   │   ├── auth_service.py
│   │   ├── security.py
│   │   └── users.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── __init__.py
│   │
│   ├── middleware/
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   └── redaction_schema.py
│   │
│   ├── services/
│   │   ├── audit_service.py
│   │   ├── redaction_service.py
│   │   └── __init__.py
│   │
│   ├── utils/
│   │   ├── redactor.py
│   │   └── __init__.py
│   │
│   └── main.py
│
├── datasets/
├── docs/
├── frontend/
│   └── streamlit_app.py
├── logs/
│   └── audit.log
├── tests/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

---

# Authentication Flow

```
User Login
      │
      ▼
Password Verification (bcrypt)
      │
      ▼
JWT Token Generation
      │
      ▼
Authenticated API Access
```

---

# Redaction Pipeline

```
Input Text
      │
      ▼
Regex Detection Engine
      │
      ▼
Identify PHI / PII
      │
      ▼
Replace Sensitive Data
      │
      ▼
Generate Audit Log
      │
      ▼
Return Redacted Response
```

---

# Supported PHI Detection

Current implementation detects:

- Person Name (Demo)
- Hospital Name
- Email Address
- Phone Number
- Aadhaar Number

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Welcome API |
| GET | `/health` | Health Check |
| POST | `/auth/login` | User Login |
| POST | `/redact/` | Redact PHI/PII |

---

# Sample Login Request

```json
{
    "username": "doctor",
    "password": "doctor123"
}
```

### Response

```json
{
    "access_token": "JWT_TOKEN",
    "token_type": "bearer"
}
```

---

# Sample Redaction Request

```json
{
    "text": "Rahul visited AIIMS Delhi. Contact: rahul@gmail.com Phone: 9876543210 Aadhaar: 1234 5678 9123"
}
```

### Response

```json
{
    "original_text": "Rahul visited AIIMS Delhi. Contact: rahul@gmail.com Phone: 9876543210 Aadhaar: 1234 5678 9123",

    "redacted_text": "[NAME_001] visited [HOSPITAL_001]. Contact: [EMAIL_001] Phone: [PHONE_001] Aadhaar: [AADHAAR_001]",

    "entities": [
        {
            "type": "PERSON",
            "value": "Rahul"
        },
        {
            "type": "HOSPITAL",
            "value": "AIIMS Delhi"
        },
        {
            "type": "EMAIL",
            "value": "rahul@gmail.com"
        },
        {
            "type": "PHONE",
            "value": "9876543210"
        },
        {
            "type": "AADHAAR",
            "value": "1234 5678 9123"
        }
    ]
}
```

---

# Audit Logging

Every redaction request is recorded inside

```
logs/audit.log
```

Example

```
[2026-07-29 13:55:02]

User=doctor

Entities=PERSON, EMAIL

Status=SUCCESS
```

---

# Installation

```bash
git clone <repository-url>

cd medshield_ai

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

# API Documentation

After running the server:

```
http://127.0.0.1:8000/docs
```

---

# Current Project Status

| Module | Status |
|---------|--------|
| Authentication | ✅ |
| JWT | ✅ |
| Password Hashing | ✅ |
| Redaction API | ✅ |
| Regex Detection | ✅ |
| Audit Logging | ✅ |
| Swagger Documentation | ✅ |

---

# Future Roadmap

- Microsoft Presidio Integration
- spaCy NLP Detection
- Redis Vault
- Reversible Pseudonymization
- Streamlit Frontend
- Docker Deployment
- Automated Testing
- CI/CD Pipeline

---

# Screenshots

Screenshots and demo images will be available inside the `docs/` directory.

---

# Author

**Rahul Singh Rawat**

B.Tech Cyber Security

Government Engineering College, Ajmer