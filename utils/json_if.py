
def json_if(payload: Mapping[str, object]) -> str | None:
    """JSON-serialize ``payload`` only when it's non-empty; else ``None``."""
    return json.dumps(payload) if payload else None

