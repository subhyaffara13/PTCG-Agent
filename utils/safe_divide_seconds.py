
def safe_divide_seconds(
    seconds: float, denominator: float, default: Optional[float] = None
) -> Optional[float]:
    """
    Safely divide seconds by denominator, handling zero division.

    Args:
        seconds: Time duration in seconds
        denominator: The divisor (e.g., number of tokens)
        default: Value to return if division by zero (defaults to None)

    Returns:
        The result of the division as a float (seconds per unit), or default if denominator is zero
    """
    if denominator <= 0:
        return default

    return float(seconds / denominator)

