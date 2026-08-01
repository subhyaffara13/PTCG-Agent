
def _validate_budget_duration(budget_duration: Optional[str]) -> None:
    """Reject budget durations that can't be parsed, are non-positive, or
    overflow date math, so a bad value can't be persisted and later crash the
    budget reset job."""
    if budget_duration is None:
        return

    from litellm.litellm_core_utils.duration_parser import duration_in_seconds
    from litellm.proxy.common_utils.timezone_utils import get_budget_reset_time

    try:
        if duration_in_seconds(budget_duration) <= 0:
            raise ValueError("budget_duration must be positive")
        get_budget_reset_time(budget_duration=budget_duration)
    except (ValueError, OverflowError):
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid budget_duration '{}'. Use a format like '1h', '24h', '7d', or '30d'.".format(
                    budget_duration
                )
            },
        )

