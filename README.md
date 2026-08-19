# MedShield AI

An AI-powered PHI/PII Redaction Pipeline designed to protect sensitive healthcare data before it is sent to Large Language Models (LLMs).

---

# Project Overview

MedShield AI is a secure middleware service that detects and redacts sensitive healthcare information before it reaches an LLM.

The project is designed to help healthcare organizations integrate AI systems while reducing the risk of exposing Personally Identifiable Information (PII) and Protected Health Information (PHI).

MedShield AI provides a complete backend pipeline with:

- Secure JWT authentication
- OAuth2 password authentication
- Role-Based Access Control (RBAC)
- Password hashing using bcrypt
- Regex-based PHI/PII detection
- Microsoft Presidio integration
- Hybrid entity detection
- Duplicate entity removal
- Dynamic placeholder generation
- Redis-backed session-based mapping
- Reversible pseudonymization
- Batch redaction
- Audit logging
- User management
- Swagger API documentation

The system follows a modular architecture so that additional detection models, security controls, deployment methods, and healthcare-specific NLP capabilities can be integrated in the future.

---

# Key Features

## Authentication & Security

- JWT Authentication
- OAuth2 Password Authentication
- Swagger UI authentication support
- Role-Based Access Control (RBAC)
- User authentication
- Password hashing using bcrypt
- Protected redaction and restoration endpoints
- Session-based isolation for sensitive mappings

## PHI/PII Detection

MedShield AI uses a hybrid detection approach combining deterministic Regex rules with Microsoft Presidio.

Supported entities include:

- Person Name
- Hospital Name
- Email Address
- Phone Number
- Aadhaar Number
- PAN Number
- Passport Number
- Date of Birth
- IPv4 Address
- Credit Card Number
- Other supported Presidio entities

## Redaction Engine

The redaction pipeline:

1. Receives sensitive text.
2. Detects entities using Regex.
3. Detects entities using Microsoft Presidio.
4. Normalizes entity types.
5. Merges results from both detection systems.
6. Removes duplicate detections.
7. Generates dynamic placeholders.
8. Stores mappings securely in Redis.
9. Replaces sensitive values with placeholders.
10. Records the redaction event in the audit log.
11. Returns the redacted response.

Example:

```text
Rahul emailed rahul@gmail.com.
```

becomes:

```text
[PERSON_001] emailed [EMAIL_001].
```

## Dynamic Placeholder Mapping

Each redaction session receives a unique session ID.

Sensitive values are mapped to placeholders such as:

```text
[PERSON_001]
[EMAIL_001]
[PHONE_001]
[PAN_001]
```

The mapping is stored in Redis using the session ID as part of the key structure.

This provides:

- Consistent placeholders for repeated values
- Session isolation
- Temporary mapping storage
- TTL-based expiration
- Reversible pseudonymization

## Reversible Restoration

Authorized users can restore placeholders back to their original values using the session ID associated with the redaction request.

Example:

```text
[PERSON_001] emailed [EMAIL_001].
```

can be restored to:

```text
Rahul emailed rahul@gmail.com.
```

The restoration process uses the Redis-backed mapping created during the original redaction session.

## Batch Redaction

The project also provides a batch redaction endpoint for processing multiple documents in a single request.

Each document receives an isolated session to prevent mappings from different documents from being mixed.

## Audit Logging

Every successful redaction operation is recorded in:

```text
logs/audit.log
```

Example:

```text
[2026-07-29 13:55:02]

User=doctor

Entities=PERSON, EMAIL, PHONE

Status=SUCCESS
```

Audit logging provides a basic trace of redaction activity and can be extended for compliance and monitoring requirements.

---

# Tech Stack

## Backend

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic

## Authentication & Security

- JWT
- python-jose
- OAuth2
- bcrypt

## AI / NLP

- Microsoft Presidio
- Regex
- Presidio Analyzer

## Data & Mapping

- Redis
- Session-based placeholder mapping
- TTL-based temporary storage

## API Documentation

- Swagger UI
- OpenAPI

## Development

- Git
- GitHub
- Python Virtual Environment

---

# Project Architecture

```text
                         Client / Application
                                  |
                                  v
                           FastAPI API Layer
                                  |
                  +---------------+---------------+
                  |                               |
                  v                               v
           Authentication                    Redaction API
                  |                               |
                  v                               v
             JWT / RBAC                  Hybrid Detection Engine
                                                  |
                              +-------------------+------------------+
                              |                                      |
                              v                                      v
                         Regex Engine                        Presidio Analyzer
                              |                                      |
                              +-------------------+------------------+
                                                  |
                                                  v
                                      Entity Merge & Normalization
                                                  |
                                                  v
                                         Redaction Engine
                                                  |
                                                  v
                                      Placeholder Mapper
                                                  |
                                                  v
                                               Redis
                                                  |
                                                  v
                                         Redacted Response
                                                  |
                                                  v
                                           Audit Logging
```

---

# Project Structure

```text
medshield_ai/
|
+-- app/
|   +-- api/
|   |   +-- routes/
|   |   |   +-- auth.py
|   |   |   +-- redact.py
|   |   +-- __init__.py
|   |   +-- dependencies.py
|   |
|   +-- auth/
|   |   +-- auth_handler.py
|   |   +-- auth_service.py
|   |   +-- security.py
|   |   +-- users.py
|   |
|   +-- core/
|   |   +-- config.py
|   |   +-- __init__.py
|   |
|   +-- middleware/
|   |
|   +-- models/
|   |
|   +-- schemas/
|   |   +-- auth_schema.py
|   |   +-- redaction_schema.py
|   |
|   +-- services/
|   |   +-- audit_service.py
|   |   +-- detection_service.py
|   |   +-- mapping_service.py
|   |   +-- redis_service.py
|   |   +-- redaction_service.py
|   |   +-- __init__.py
|   |
|   +-- utils/
|   |   +-- redactor.py
|   |   +-- __init__.py
|   |
|   +-- main.py
|
+-- datasets/
+-- docs/
+-- frontend/
|   +-- streamlit_app.py
+-- logs/
|   +-- audit.log
+-- tests/
+-- .env.example
+-- .gitignore
+-- README.md
+-- requirements.txt
+-- run.py
```

---

# Authentication Flow

```text
                         User Login
                             |
                             v
                    Username & Password
                             |
                             v
                    Password Verification
                          (bcrypt)
                             |
                             v
                     JWT Token Generation
                             |
                             v
                    Swagger / API Client
                             |
                             v
                  Authorization: Bearer Token
                             |
                             v
                    JWT Validation + RBAC
                             |
                             v
                   Protected API Endpoint
```

---

# Redaction Pipeline

```text
                         Input Text
                             |
                             v
                      Regex Detection
                             |
                             v
                    Microsoft Presidio
                        Detection
                             |
                             v
                    Entity Normalization
                             |
                             v
                     Duplicate Removal
                             |
                             v
                    Entity Merge Process
                             |
                             v
                     Hybrid Redaction
                           Engine
                             |
                             v
                   Dynamic Placeholder
                       Generation
                             |
                             v
                      Redis Mapping
                             |
                             v
                   Redacted Response
                             |
                             v
                    Audit Logging
```

---

# Restoration Pipeline

```text
                       Redacted Text
                             |
                             v
                         Session ID
                             |
                             v
                    Redis Mapping
                             |
                             v
                 Placeholder Lookup
                             |
                             v
                 Original Value Lookup
                             |
                             v
                    Restored Text
```

---

# Supported PHI/PII Detection

The current detection engine supports the following categories:

| Entity              | Detection Method    |
|---------------------|---------------------|
| Person Name         | Presidio            |
| Hospital Name       | Regex               |
| Email Address       | Regex + Presidio    |
| Phone Number        | Regex + Presidio    |
| Aadhaar Number      | Regex               |
| PAN Number          | Regex               |
| Passport Number     | Regex               |
| Date of Birth       | Regex               |
| IPv4 Address        | Regex + Presidio    |
| Credit Card Number  | Presidio            |

The hybrid approach allows deterministic patterns to be combined with NLP-based entity recognition.

---
# API Endpoints

| Method | Endpoint             | Description              |
|--------|----------------------|--------------------------|
| GET    | `/`                  | Welcome API              |
| GET    | `/health`            | Health Check             |
| GET    | `/version`           | Application Version      |
| POST   | `/auth/login`        | User Login               |
| GET    | `/auth/me`           | Current User             |
| POST   | `/redact/`           | Redact PHI/PII           |
| POST   | `/redact/batch`      | Batch Redaction          |
| POST   | `/redact/restore`    | Restore Redacted Values  |
| GET    | `/audit/logs`        | View Audit Logs          |
| GET    | `/audit/stats`       | Audit Statistics         |
| GET    | `/users/`            | List Users               |
| GET    | `/users/{username}`  | User Details             |


Protected endpoints require a valid JWT bearer token.

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
    "text": "Rahul visited AIIMS Delhi. Contact: rahul@gmail.com Phone: 9876543210 PAN: ABCDE1234F"
}
```

### Response

```json
{
    "session_id": "a55901fe-42a9-470f-947d-fc1ae70cc0c8",
    "original_text": "Rahul visited AIIMS Delhi. Contact: rahul@gmail.com Phone: 9876543210 PAN: ABCDE1234F",
    "redacted_text": "[PERSON_001] visited [HOSPITAL_001]. Contact: [EMAIL_001] Phone: [PHONE_001] PAN: [PAN_001]",
    "entities": [
        {
            "type": "EMAIL",
            "value": "rahul@gmail.com"
        },
        {
            "type": "PHONE",
            "value": "9876543210"
        },
        {
            "type": "PAN",
            "value": "ABCDE1234F"
        },
        {
            "type": "PERSON",
            "value": "Rahul"
        }
    ]
}
```

---

# Sample Restoration Request

```json
{
    "session_id": "a55901fe-42a9-470f-947d-fc1ae70cc0c8",
    "text": "[PERSON_001] visited [HOSPITAL_001]. Contact: [EMAIL_001]"
}
```

### Response

```json
{
    "session_id": "a55901fe-42a9-470f-947d-fc1ae70cc0c8",
    "restored_text": "Rahul visited AIIMS Delhi. Contact: rahul@gmail.com"
}
```

---

# Redis Session Mapping

Redis stores temporary mappings using a session-specific namespace.

Example structure:

```text
medshield:<session_id>:forward:<entity_type>:<value>
medshield:<session_id>:reverse:<placeholder>
medshield:<session_id>:counter:<entity_type>
```

Example:

```text
PERSON + Rahul
      |
      v
[PERSON_001]
```

The reverse mapping allows:

```text
[PERSON_001]
      |
      v
    Rahul
```

Mappings use a TTL to limit their lifetime and reduce unnecessary long-term storage of sensitive information.

---

# Security Considerations

MedShield AI follows several security principles:

- Sensitive API endpoints require authentication.
- Role-based authorization is applied to protected operations.
- Passwords are stored using secure hashing.
- JWT tokens are used for authenticated API access.
- Redaction mappings are isolated by session.
- Redis mappings use temporary TTL-based storage.
- Sensitive values are not used as permanent application identifiers.
- Audit logging provides traceability of redaction operations.
- Configuration values are managed through environment variables.

The system is designed as a security layer before sensitive healthcare data is passed to downstream AI services.

---

# Audit Logging

Every successful redaction operation is recorded inside:

```text
logs/audit.log
```

Example:

```text
[2026-07-29 13:55:02]

User=doctor

Entities=PERSON, EMAIL, PHONE

Status=SUCCESS
```

Audit information can later be extended to include request IDs, timestamps, IP information, processing duration, and compliance-specific metadata.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Rahul181512/medshield_ai.git
```

Move into the project directory:

```bash
cd medshield_ai
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables using:

```text
.env.example
```

Start the application:

```bash
uvicorn app.main:app --reload
```

---

# API Documentation

After starting the server, Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI specification is available through the FastAPI application.

---

# Project Status

## Backend

- [x] FastAPI Backend
- [x] REST APIs
- [x] Health API
- [x] Version API
- [x] Modular Service Architecture
- [x] Swagger / OpenAPI Documentation

## Authentication & Security

- [x] JWT Authentication
- [x] OAuth2 Authentication
- [x] Role-Based Access Control
- [x] Password Hashing with bcrypt
- [x] Protected API Endpoints
- [x] Environment-based Configuration
- [x] Session-based Isolation

## PHI/PII Detection

- [x] Regex Detection
- [x] Microsoft Presidio Integration
- [x] Hybrid Detection Engine
- [x] Entity Normalization
- [x] Duplicate Entity Removal
- [x] Multiple PHI/PII Entity Types

## Redaction & Privacy

- [x] Hybrid Redaction Engine
- [x] Dynamic Placeholder Mapping
- [x] Redis-backed Mapping
- [x] Session-based Mapping
- [x] TTL-based Mapping Expiration
- [x] Reversible Pseudonymization
- [x] Restoration API
- [x] Batch Redaction API

## Monitoring & Management

- [x] Audit Logging
- [x] Audit Statistics
- [x] User Management APIs
- [x] Request-level Redaction Tracking

---

# Testing & Validation

The project has been validated through API-level testing using Swagger UI and direct API requests.

The main workflow has been tested for:

- User authentication
- JWT authorization
- PHI/PII detection
- Hybrid entity detection
- Redaction
- Dynamic placeholder generation
- Redis mapping
- Session-based restoration
- Batch processing
- Audit logging

Example validation flow:

```text
Login
  |
  v
JWT Token
  |
  v
Redaction Request
  |
  v
Entity Detection
  |
  v
Placeholder Mapping
  |
  v
Redis Storage
  |
  v
Redacted Response
  |
  v
Restoration Request
  |
  v
Original Text
```

---

# Project Completion Summary

MedShield AI has been developed as a complete backend prototype for secure PHI/PII protection in AI-enabled healthcare workflows.

The final implementation combines:

```text
FastAPI
   +
JWT / OAuth2
   +
RBAC
   +
Regex
   +
Microsoft Presidio
   +
Hybrid Detection
   +
Redis
   +
Dynamic Placeholder Mapping
   +
Reversible Pseudonymization
   +
Audit Logging
```

This provides a complete foundation for intercepting sensitive healthcare text, identifying sensitive entities, replacing them with temporary placeholders, securely storing the mappings, and restoring the original information when authorized.

---

# Future Improvements

Although the core project is complete, several enhancements can make MedShield AI more powerful, secure, scalable, and easier to use.

## Advanced NLP Detection

Future versions can integrate:

- spaCy custom NER models
- Healthcare-specific NLP models
- Clinical entity recognition
- Custom Presidio recognizers
- Context-aware entity detection
- Confidence scoring and threshold-based decisions

This can improve detection accuracy for complex medical documents.

## Improved Security

Future security improvements may include:

- API rate limiting
- Refresh token rotation
- Multi-factor authentication
- Stronger session management
- Encryption of sensitive Redis data
- Key rotation
- Secrets management using Vault or cloud secret managers
- Fine-grained RBAC permissions
- Security event monitoring

## Better Privacy Controls

Future versions can introduce:

- Configurable mapping TTL
- Automatic session cleanup
- Secure key management
- Configurable anonymization strategies
- Permanent anonymization mode
- Configurable masking and tokenization
- Data retention policies

## Scalability

The system can be extended with:

- Docker containerization
- Docker Compose
- Kubernetes deployment
- Redis clustering
- Horizontal API scaling
- Background processing using Celery or similar task queues
- Cloud deployment

## User Interface

A dedicated Streamlit dashboard can provide:

- Document upload
- Text redaction
- Redaction preview
- Entity statistics
- Session management
- Audit log visualization
- Restoration workflow
- System health information

## Monitoring & Observability

Future versions can integrate:

- Prometheus
- Grafana
- Structured logging
- Application performance monitoring
- Centralized log management
- Security event monitoring
- Alerting

## CI/CD & Quality

The development pipeline can be improved with:

- Automated unit tests
- Integration testing
- API testing
- Security testing
- GitHub Actions
- Automated linting
- Code quality checks
- Dependency vulnerability scanning
- Automated deployment

---

# Roadmap

```text
                         CURRENT
                            |
                            v
                  Core MedShield AI
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
          Security       Detection      Privacy
              |             |             |
              v             v             v
          JWT/RBAC       Presidio       Redis
          OAuth2        + Regex         Mapping
              |             |             |
              +-------------+-------------+
                            |
                            v
                    Reversible Redaction
                            |
                            v
                     Future Expansion
                            |
          +-----------------+-----------------+
          |                 |                 |
          v                 v                 v
       Advanced NLP      Cloud Scale       Dashboard
          |                 |                 |
          v                 v                 v
       spaCy / NER       Docker/K8s       Streamlit
          |                 |                 |
          +-----------------+-----------------+
                            |
                            v
                  Production-Ready Platform
```

---

# Screenshots

Screenshots and demonstration images can be stored inside:

```text
docs/
```

The documentation directory can contain Swagger screenshots, redaction examples, authentication flows, and dashboard demonstrations.

---

# Author

**Rahul Singh Rawat**

B.Tech Cyber Security

Government Engineering College, Ajmer
