
def _convert_aware_datetime(
    value: dt.datetime | dt.timedelta | float | None,
) -> Any:
    """Convert aware datetime to naive datetime and pass through any other type."""
    if value is None:
        return None

    import datetime as dt

    if isinstance(value, dt.datetime) and value.tzinfo is not None:
        value = dt.datetime.fromtimestamp(value.timestamp())
    return value

