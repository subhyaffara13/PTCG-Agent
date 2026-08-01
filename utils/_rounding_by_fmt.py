
def _rounding_by_fmt(format: str, value: float) -> float | int:
    """Round a number according to the string format provided.

    The string format is the old printf-style string formatting.

    If we are using a format which truncates the value, such as "%d" or "%i", the
    returned value will be of type `int`.

    If we are using a format which rounds the value, such as "%.2f" or even "%.0f",
    we will return a float.
    """
    result = format % value

    try:
        value = int(result)
    except ValueError:
        value = float(result)

    return value

