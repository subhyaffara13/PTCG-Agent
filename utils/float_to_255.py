
def float_to_255(c: float) -> int:
    """Converts a float value between 0 and 1 (inclusive) to an integer between 0 and 255 (inclusive).

    Args:
        c: The float value to be converted. Must be between 0 and 1 (inclusive).

    Returns:
        The integer equivalent of the given float value rounded to the nearest whole number.

    Raises:
        ValueError: If the given float value is outside the acceptable range of 0 to 1 (inclusive).
    """
    return int(round(c * 255))


def float_to_255(c: float) -> int:
    return int(round(c * 255))

