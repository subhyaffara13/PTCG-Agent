
def _json_or_none(value: object) -> str | None:
    """JSON-serialize ``value`` (already-string values pass through). ``None`` on failure."""
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, default=str)
    except Exception:
        return None

