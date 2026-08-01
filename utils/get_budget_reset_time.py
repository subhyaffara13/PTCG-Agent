
def get_budget_reset_time(budget_duration: str) -> datetime:
    """
    Get the budget reset time based on the configured timezone.
    Falls back to UTC if not specified.
    """

    reset_at = get_next_standardized_reset_time(
        duration=budget_duration,
        current_time=datetime.now(timezone.utc),
        timezone_str=get_budget_reset_timezone(),
    )
    return reset_at

