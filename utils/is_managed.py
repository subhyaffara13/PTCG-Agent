
def is_managed(value: str) -> bool:
    """Return ``True`` iff *value* decodes to a passthrough managed ID."""
    return decode(value) is not None

