import logging

# Set up basic logger
# - Add timestamps, log levels
# - Optionally log to file

# Use logger across main.py, redact.py, etc.
# Configure logger
logger = logging.getLogger("spacy_redactor")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

# Console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# Optional: File handler (uncomment to enable file logging)
fh = logging.FileHandler("spacy_redactor.log")
fh.setFormatter(formatter)
logger.addHandler(fh)
