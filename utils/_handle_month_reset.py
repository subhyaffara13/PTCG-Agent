
def _handle_month_reset(
    current_time: datetime, base_midnight: datetime, value: int
) -> datetime:
    """
    Handle monthly reset times. For monthly resets, we always reset at the start of the next month.

    Args:
        current_time: Current datetime
        base_midnight: Midnight of current day
        value: Number of months (currently only supports 1 month resets)

    Returns:
        datetime: First day of next month at midnight
    """
    if value != 1:
        raise ValueError("Monthly resets currently only support 1 month intervals")

    # Get the first day of next month
    if current_time.month == 12:
        next_month = 1
        next_year = current_time.year + 1
    else:
        next_month = current_time.month + 1
        next_year = current_time.year

    return datetime(
        year=next_year,
        month=next_month,
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=current_time.tzinfo,
    )

