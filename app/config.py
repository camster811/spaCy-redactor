import os
from dotenv import load_dotenv

# Load .env file (dotenv)

# Define config variables (DEBUG, API_TITLE, LOG_LEVEL)

# Central place to manage app-wide settings
load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
API_TITLE = os.getenv("API_TITLE", "spaCy Redactor API")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
