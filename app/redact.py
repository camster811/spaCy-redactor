# Load and initialize spaCy NLP model
import spacy
from inference import annotate_redaction

nlp = spacy.load("en_core_web_sm")  # Load the spaCy model for NER


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

    metadata = annotate_redaction(metadata)  # Annotate metadata with reasons
    return redacted_text, metadata
