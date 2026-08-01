
def get_next_standardized_reset_time(
    duration: str, current_time: datetime, timezone_str: str = "UTC"
) -> datetime:
    """
    Get the next standardized reset time based on the duration.

    All durations will reset at predictable intervals, aligned from the current time:
    - Nd: If N=1, reset at next midnight; if N>1, reset every N days from now
    - Nh: Every N hours, aligned to hour boundaries (e.g., 1:00, 2:00)
    - Nm: Every N minutes, aligned to minute boundaries (e.g., 1:05, 1:10)
    - Ns: Every N seconds, aligned to second boundaries

    Parameters:
    - duration: Duration string (e.g. "30s", "30m", "30h", "30d")
    - current_time: Current datetime
    - timezone_str: Timezone string (e.g. "UTC", "US/Eastern", "Asia/Kolkata")

    Returns:
    - Next reset time at a standardized interval in the specified timezone
    """
    # Set up timezone and normalize current time
    current_time, tz = _setup_timezone(current_time, timezone_str)

    # Parse duration
    value, unit = _parse_duration(duration)
    if value is None:
        # Fall back to default if format is invalid
        return current_time.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)

    # Midnight of the current day in the specified timezone
    base_midnight = current_time.replace(hour=0, minute=0, second=0, microsecond=0)

    # Handle different time units
    if unit == "d":
        return _handle_day_reset(current_time, base_midnight, value, tz)
    elif unit == "w":
        return _handle_day_reset(current_time, base_midnight, value * 7, tz)
    elif unit == "h":
        return _handle_hour_reset(current_time, base_midnight, value)
    elif unit == "m":
        return _handle_minute_reset(current_time, base_midnight, value)
    elif unit == "s":
        return _handle_second_reset(current_time, base_midnight, value)
    elif unit == "mo":
        return _handle_month_reset(current_time, base_midnight, value)
    else:
        # Unrecognized unit, default to next midnight
        return base_midnight + timedelta(days=1)

