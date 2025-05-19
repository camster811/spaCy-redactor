# Accept NLP output or entity list

# Define rule engine or manual rule mapping
# - e.g., if entity type == EMAIL and ORG → high sensitivity

# Annotate each redacted entity with reason
# - Reason could be "Direct Identifier", "Inferred Role", etc.

# Return extended metadata list with reasons


def annotate_redaction(entities):
    """
    Annotate a redacted entity with a reason for redaction.
    """
    for ent in entities:
        if ent["type"] == "PERSON":
            ent["reason"] = "Direct Identifier"
        elif ent["type"] == "ORG":
            ent["reason"] = "Inferred Role"
        elif ent["type"] == "GPE":
            ent["reason"] = "Location Identifier"
        elif ent["type"] == "DATE":
            ent["reason"] = "Date Reference"
        elif ent["type"] == "TIME":
            ent["reason"] = "Time Reference"
        elif ent["type"] == "EMAIL":
            ent["reason"] = "Email Address"
        elif ent["type"] == "PHONE":
            ent["reason"] = "Phone Number"
        else:
            ent["reason"] = "General Redaction"
    return entities
