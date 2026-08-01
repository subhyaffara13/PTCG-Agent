
def _handle_day_reset(
    current_time: datetime, base_midnight: datetime, value: int, tz: tzinfo
) -> datetime:
    """Handle day-based reset times."""
    # Handle zero value - immediate expiration
    if value == 0:
        return current_time

    if value == 1:  # Daily reset at midnight
        return base_midnight + timedelta(days=1)
    elif value == 7:  # Weekly reset on Monday at midnight
        days_until_monday = (7 - current_time.weekday()) % 7
        if days_until_monday == 0:  # If today is Monday
            days_until_monday = 7
        return base_midnight + timedelta(days=days_until_monday)
    elif value == 30:  # Monthly reset on 1st at midnight
        # Get 1st of next month at midnight
        if current_time.month == 12:
            next_reset = datetime(
                year=current_time.year + 1,
                month=1,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=tz,
            )
        else:
            next_reset = datetime(
                year=current_time.year,
                month=current_time.month + 1,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=tz,
            )
        return next_reset
    else:  # Custom day value - next interval is value days from current
        return current_time.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=value)

