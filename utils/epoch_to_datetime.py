
def epoch_to_datetime(t: int | None) -> datetime | None:
    """Convert epoch time to a UTC datetime."""
    if t is None:
        return None
    return datetime.fromtimestamp(t, tz=timezone.utc)

