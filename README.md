# MedShield AI

An AI-powered PHI/PII Redaction Pipeline designed to protect sensitive healthcare data before it is sent to Large Language Models (LLMs).

---

# Project Overview

MedShield AI is a secure middleware service that detects and redacts sensitive healthcare information before it reaches an LLM.

The project focuses on protecting Personally Identifiable Information (PII) and Protected Health Information (PHI) while allowing healthcare organizations to safely integrate AI systems into their workflows.

The current implementation provides secure JWT authentication, OAuth2 login, role-based access control (RBAC), audit logging, and a hybrid PHI/PII detection engine powered by Regex and Microsoft Presidio. The backend follows a modular architecture that is designed for future enhancements such as dynamic placeholder mapping, medical NLP using spaCy, and reversible anonymization.

---

# Features

## Implemented

- FastAPI REST API
- JWT Authentication
- OAuth2 Authentication (Swagger UI)
- Password Hashing (bcrypt)
- Role-Based Access Control (RBAC)
- User Authentication
- Regex-based PHI/PII Detection
- Microsoft Presidio Integration
- Hybrid Detection Engine (Regex + Presidio)
- Duplicate Entity Removal
- Hybrid Redaction Engine
- Batch Redaction API
- Audit Logging
- User Management APIs
- Swagger API Documentation
- Modular Service Layer

---

## Planned

- Dynamic Placeholder Mapping
- Entity Mapping Engine
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

### AI / NLP 

- Microsoft Presidio
- Regular Expressions (Regex)
- spaCy (Upcoming)

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
|    |  ├── detection_service.py 
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
               Regex Detection
                       │
                       ▼
          Microsoft Presidio Detection
                       │
                       ▼
           Merge & Normalize Entities
                       │
                       ▼
             Hybrid Redaction Engine
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

- Person Name
- Hospital Name
- Email Address
- Phone Number
- Aadhaar Number
- PAN Number
- Passport Number
- Date of Birth
- IPv4 Address

---

# API Endpoints

| Method | Endpoint            | Description         |
| ------ | ------------------- | ------------------- |
| GET    | `/`                 | Welcome API         |
| GET    | `/health`           | Health Check        |
| GET    | `/version`          | Application Version |
| POST   | `/auth/login`       | User Login          |
| GET    | `/auth/me`          | Current User        |
| POST   | `/redact/`          | Redact PHI/PII      |
| POST   | `/redact/batch`     | Batch Redaction     |
| GET    | `/audit/logs`       | View Audit Logs     |
| GET    | `/audit/stats`      | Audit Statistics    |
| GET    | `/users/`           | List Users          |
| GET    | `/users/{username}` | User Details        |

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
git clone https://github.com/Rahul181512/medshield_ai.git

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

## Current Project Status

### Backend
- ✅ FastAPI Backend
- ✅ REST APIs
- ✅ Health & Version APIs
- ✅ Swagger API Documentation

### Authentication & Security
- ✅ JWT Authentication
- ✅ OAuth2 Authentication
- ✅ Role-Based Access Control (RBAC)
- ✅ Password Hashing (bcrypt)
- ✅ User Authentication

### PHI/PII Detection
- ✅ Regex-based PHI/PII Detection
- ✅ Microsoft Presidio Integration
- ✅ Hybrid Detection Engine
- ✅ Duplicate Entity Removal
- ✅ Hybrid Redaction Engine
- ✅ Batch Redaction API

### Monitoring
- ✅ Audit Logging
- ✅ User Management APIs

---

# Future Roadmap

- Dynamic Placeholder Mapping
- Reverse Mapping
- spaCy NLP Detection
- Redis Vault
- Reversible Pseudonymization
- Streamlit Frontend
- Docker Deployment
- Automated Testing
- CI/CD Pipeline

---

pending...
# Screenshots

Screenshots and demo images will be available inside the `docs/` directory.

---

# Author

**Rahul Singh Rawat**

B.Tech Cyber Security

Government Engineering College, Ajmer