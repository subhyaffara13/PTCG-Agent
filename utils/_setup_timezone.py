
def _setup_timezone(
    current_time: datetime, timezone_str: str = "UTC"
) -> Tuple[datetime, tzinfo]:
    """Set up timezone and normalize current time to that timezone."""
    try:
        if timezone_str is None:
            tz: tzinfo = timezone.utc
        else:
            tz = ZoneInfo(timezone_str)
    except Exception:
        # If timezone is invalid, fall back to UTC
        tz = timezone.utc

    # Convert current_time to the target timezone
    if current_time.tzinfo is None:
        # Naive datetime - assume it's UTC
        utc_time = current_time.replace(tzinfo=timezone.utc)
        current_time = utc_time.astimezone(tz)
    else:
        # Already has timezone - convert to target timezone
        current_time = current_time.astimezone(tz)

    return current_time, tz

