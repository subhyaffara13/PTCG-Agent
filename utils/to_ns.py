
def to_ns(value: datetime | float | int | None) -> int | None:
    """Coerce a datetime / epoch value to integer nanoseconds."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return int(value.timestamp() * 1e9)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return int(float(value) * 1e9)
    return None

