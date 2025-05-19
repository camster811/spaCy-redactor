# spaCy-redactor

An async redaction backend service using FastAPI, spaCy NLP, asyncio, and CI/CD workflows. Built to simulate a system for identifying and redacting sensitive information in text documents.

- ✅ Named Entity Redaction via spaCy
- 🧠 Logical Inference on Redactions
- ⚡ Async background processing using `asyncio`
- 🧪 Automated tests with `pytest` + `httpx`
- 🐳 Dockerized setup with CI/CD via GitHub Actions

# Project Structure
```
spacy-redactor/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app w/ routes
│   ├── models.py            # Pydantic request/response schemas
│   ├── redact.py            # Core spaCy NLP logic
│   ├── inference.py         # Logical inference reasoning on entities
│   ├── tasks.py             # asyncio job queue, background tasks
│   ├── config.py            # Config & env setup
│   └── logger.py            # Logging setup
│
├── tests/
│   ├── __init__.py
│   ├── test_redact.py       # Unit tests for redact logic
│   ├── test_inference.py    # Unit tests for inference module
│   ├── test_api.py          # Async API tests using httpx
│   └── conftest.py          # Test fixtures
│
├── Dockerfile               # Container build for spaCy + FastAPI
├── docker-compose.yml       # Compose multi-service setup (optional)
├── requirements.txt         # App dependencies
├── .env                     # environment variables
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions pipeline
└── README.md
```
# Steps
source .venv/bin/activate
cd app/
python main.py
navigate to http://127.0.0.1:8000/docs and enter text or alternatively use curl commands
ex. 
1. 
curl -X POST "http://127.0.0.1:8000/submit" -H "Content-Type: application/json" -d '{"text": "John Mark met with Jane Doe in London last year."}'
curl -X POST "http://127.0.0.1:8000/submit" -H "Content-Type: application/json" -d '{"text": "The CEO of Acme Corp visited Paris on January 1st, 2022."}'
2. 
curl "http://127.0.0.1:8000/status/<job_id>"
3. 
curl "http://127.0.0.1:8000/result/<job_id>"

# Exapmle result
![example_usage](https://github.com/user-attachments/assets/71d808d0-d31e-4da1-be28-3af356c47f0b)

