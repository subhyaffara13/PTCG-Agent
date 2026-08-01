
def _ensure_datetime_utc(timestamp: datetime) -> datetime:
    """Helper to ensure datetime is in UTC"""
    timestamp = timestamp.astimezone(timezone.utc)
    return timestamp

