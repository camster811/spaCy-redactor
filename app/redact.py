# Load and initialize spaCy NLP model
import spacy
from inference import annotate_redaction
import re

nlp = spacy.load("en_core_web_sm")  # Load the spaCy model for NER

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"


# Define function to process input text
# - Perform NER on text
# - Identify sensitive entities (PERSON, ORG, etc.)
# - Replace entities with [REDACTED] or similar
# - Track redaction metadata (type, span, reason)


# Return redacted text and metadata
def sanitize_text(text):
    doc = nlp(text)
    redacted_text = text
    metadata = []
    offset = 0  # Track offset due to replacement length changes

    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE", "DATE", "TIME"]:
            start, end = ent.start_char + offset, ent.end_char + offset
            original = redacted_text[start:end]
            metadata.append(
                {
                    "type": ent.label_,
                    "span": [start, end],
                    "text": original,
                }
            )
            # Replace entity with [REDACTED]
            redacted_text = redacted_text[:start] + "[REDACTED]" + redacted_text[end:]

            # Update offset for next replacements
            offset += len("[REDACTED]") - (end - start)

    # Redact email addresses
    for match in re.finditer(EMAIL_REGEX, redacted_text):
        start, end = match.span()
        metadata.append(
            {
                "type": "EMAIL",
                "span": [start, end],
                "text": redacted_text[start:end],
            }
        )
        redacted_text = redacted_text[:start] + "[REDACTED]" + redacted_text[end:]
        offset += len("[REDACTED]") - (end - start)

    # Redact phone numbers
    for match in re.finditer(PHONE_REGEX, redacted_text):
        start, end = match.span()
        metadata.append(
            {
                "type": "PHONE",
                "span": [start, end],
                "text": redacted_text[start:end],
            }
        )
        redacted_text = redacted_text[:start] + "[REDACTED]" + redacted_text[end:]
        offset += len("[REDACTED]") - (end - start)

    metadata = annotate_redaction(metadata)
    return redacted_text, metadata
