
def _handle_minute_reset(
    current_time: datetime, base_midnight: datetime, value: int
) -> datetime:
    """Handle minute-based reset times."""
    # Handle zero value - immediate expiration
    if value == 0:
        return current_time

    current_hour = current_time.hour
    current_minute = current_time.minute
    current_second = current_time.second
    current_microsecond = current_time.microsecond

    # Calculate next minute aligned with the value
    if current_second == 0 and current_microsecond == 0:
        next_minute = (
            current_minute + value - (current_minute % value)
            if current_minute % value != 0
            else current_minute + value
        )
    else:
        next_minute = (
            current_minute + value - (current_minute % value)
            if current_minute % value != 0
            else current_minute + value
        )

    # Handle hour rollover
    next_hour = current_hour + (next_minute // 60)
    next_minute = next_minute % 60

    # Handle overnight case
    if next_hour >= 24:
        next_hour = next_hour % 24
        next_day = base_midnight + timedelta(days=1)
        return next_day.replace(
            hour=next_hour, minute=next_minute, second=0, microsecond=0
        )

    return current_time.replace(
        hour=next_hour, minute=next_minute, second=0, microsecond=0
    )

