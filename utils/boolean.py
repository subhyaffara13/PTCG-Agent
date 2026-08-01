
def boolean(raw: str | bool) -> Bool:
    """Turn `true` or `false` into a boolean item."""
    return item(raw == "true" if isinstance(raw, str) else raw)

