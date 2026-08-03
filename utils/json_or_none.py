import json

def json_or_none(value: object) -> str | None:
    """JSON-serialize ``value`` (falling back to ``str``); ``None`` on failure."""
    try:
        return json.dumps(value, default=str)
    except Exception:
        return None

