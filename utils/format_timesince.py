import time

def format_timesince(ts: float) -> str:
    """Format timestamp in seconds into a human-readable string, relative to now.

    Vaguely inspired by Django's `timesince` formatter.
    """
    _TIMESINCE_CHUNKS = (
        # Label, divider, max value
        ("second", 1, 60),
        ("minute", 60, 60),
        ("hour", 60 * 60, 24),
        ("day", 60 * 60 * 24, 6),
        ("week", 60 * 60 * 24 * 7, 6),
        ("month", 60 * 60 * 24 * 30, 11),
        ("year", 60 * 60 * 24 * 365, None),
    )
    delta = time.time() - ts
    if delta < 20:
        return "a few seconds ago"
    for label, divider, max_value in _TIMESINCE_CHUNKS:  # noqa: B007
        value = round(delta / divider)
        if max_value is not None and value <= max_value:
            break
    return f"{value} {label}{'s' if value > 1 else ''} ago"

