import json

def stringify_message(message: object) -> str | None:
    """JSON-serialize a chat message dict; ``None`` if not a dict or on failure."""
    if not isinstance(message, dict):
        return None
    try:
        return json.dumps(message, default=str)
    except Exception:
        return None

