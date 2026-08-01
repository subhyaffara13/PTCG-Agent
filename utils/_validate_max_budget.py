
def _validate_max_budget(max_budget: Optional[float]) -> None:
    """
    Validate that max_budget is not negative.

    Args:
        max_budget: The max_budget value to validate

    Raises:
        HTTPException: If max_budget is negative
    """
    if max_budget is not None and (not math.isfinite(max_budget) or max_budget < 0):
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"max_budget must be a non-negative finite number. Received: {max_budget}"
            },
        )

