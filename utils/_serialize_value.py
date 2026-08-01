
def _serialize_value(v: object) -> object:
    """Recursively serialize a value to be JSON-compatible."""
    if isinstance(v, datetime.datetime):
        return v.isoformat()
    elif isinstance(v, dict):
        return {key: _serialize_value(val) for key, val in v.items() if val is not None}
    elif isinstance(v, list):
        return [_serialize_value(item) for item in v]
    return v

