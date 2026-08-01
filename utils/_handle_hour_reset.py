
def _handle_hour_reset(
    current_time: datetime, base_midnight: datetime, value: int
) -> datetime:
    """Handle hour-based reset times."""
    # Handle zero value - immediate expiration
    if value == 0:
        return current_time

    current_hour = current_time.hour
    current_minute = current_time.minute
    current_second = current_time.second
    current_microsecond = current_time.microsecond

    # Calculate next hour aligned with the value
    if current_minute == 0 and current_second == 0 and current_microsecond == 0:
        next_hour = (
            current_hour + value - (current_hour % value)
            if current_hour % value != 0
            else current_hour + value
        )
    else:
        next_hour = (
            current_hour + value - (current_hour % value)
            if current_hour % value != 0
            else current_hour + value
        )

    # Handle overnight case
    if next_hour >= 24:
        next_hour = next_hour % 24
        next_day = base_midnight + timedelta(days=1)
        return next_day.replace(hour=next_hour)

    return current_time.replace(hour=next_hour, minute=0, second=0, microsecond=0)

