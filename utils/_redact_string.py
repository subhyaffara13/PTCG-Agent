
def _redact_string(value: str) -> str:
    if not _ENABLE_SECRET_REDACTION:
        return value
    return redact_string(value)

