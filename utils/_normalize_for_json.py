
def _normalize_for_json(value):
    """Recursively convert tuples to lists. Other types pass through."""
    if isinstance(value, tuple):
        return [_normalize_for_json(v) for v in value]
    if isinstance(value, list):
        return [_normalize_for_json(v) for v in value]
    if isinstance(value, dict):
        return {k: _normalize_for_json(v) for k, v in value.items()}
    return value

