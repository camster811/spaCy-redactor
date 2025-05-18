# spaCy-redactor
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
├── .env.example             # Example environment variables
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions pipeline
└── README.md
