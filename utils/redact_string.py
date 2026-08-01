
def redact_string(value: str) -> str:
    """Scrub known secret/credential patterns from *value* and return the result."""
    return _SECRET_RE.sub(_REDACTED, value)

