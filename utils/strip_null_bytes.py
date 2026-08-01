
def strip_null_bytes(value: str) -> str:
    """Strip NUL bytes, which PostgreSQL text/jsonb columns reject (error 22P05)."""
    return value.replace("\x00", "")

