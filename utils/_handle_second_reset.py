
def _handle_second_reset(
    current_time: datetime, base_midnight: datetime, value: int
) -> datetime:
    """Handle second-based reset times."""
    # Handle zero value - immediate expiration
    if value == 0:
        return current_time

    current_hour = current_time.hour
    current_minute = current_time.minute
    current_second = current_time.second
    current_microsecond = current_time.microsecond

    # Calculate next second aligned with the value
    if current_microsecond == 0:
        next_second = (
            current_second + value - (current_second % value)
            if current_second % value != 0
            else current_second + value
        )
    else:
        next_second = (
            current_second + value - (current_second % value)
            if current_second % value != 0
            else current_second + value
        )

    # Handle minute rollover
    additional_minutes = next_second // 60
    next_second = next_second % 60
    next_minute = current_minute + additional_minutes

    # Handle hour rollover
    next_hour = current_hour + (next_minute // 60)
    next_minute = next_minute % 60

    # Handle overnight case
    if next_hour >= 24:
        next_hour = next_hour % 24
        next_day = base_midnight + timedelta(days=1)
        return next_day.replace(
            hour=next_hour, minute=next_minute, second=next_second, microsecond=0
        )

    return current_time.replace(
        hour=next_hour, minute=next_minute, second=next_second, microsecond=0
    )

