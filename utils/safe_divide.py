from typing import Union

def safe_divide(
    numerator: Union[int, float],
    denominator: Union[int, float],
    default: Union[int, float] = 0,
) -> Union[int, float]:
    """
    Safely divide two numbers, returning a default value if denominator is zero.

    Args:
        numerator: The number to divide
        denominator: The number to divide by
        default: Value to return if denominator is zero (defaults to 0)

    Returns:
        The result of numerator/denominator, or default if denominator is zero
    """
    if denominator == 0:
        return default
    return numerator / denominator

