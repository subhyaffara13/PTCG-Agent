
def _redact_sensitive_body(body: str) -> str:
    """Redact OAuth credential values from a JSON or form-urlencoded request body string."""
    for pattern, replacement in _SENSITIVE_BODY_PATTERNS:
        body = pattern.sub(replacement, body)
    return body

