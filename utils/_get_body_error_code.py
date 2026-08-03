import json

def _get_body_error_code(error_str: str) -> int | None:
    """Return error.code from a JSON error body, or None if not parseable."""
    try:
        body = json.loads(error_str)
        code = body.get("error", {}).get("code")
        return int(code) if code is not None else None
    except Exception:
        return None

