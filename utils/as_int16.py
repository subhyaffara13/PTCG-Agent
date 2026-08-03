import math


def asInt16(array):
    """Round a list of floats to 16-bit signed integers.

    Args:
        array: List of float values.

    Returns:
        A list of rounded integers.
    """
    return [int(math.floor(i + 0.5)) for i in array]

