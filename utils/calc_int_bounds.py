
def calcIntBounds(array, round=otRound):
    """Calculate the integer bounding rectangle of a 2D points array.

    Values are rounded to closest integer towards ``+Infinity`` using the
    :func:`fontTools.misc.fixedTools.otRound` function by default, unless
    an optional ``round`` function is passed.

    Args:
        array: A sequence of 2D tuples.
        round: A rounding function of type ``f(x: float) -> int``.

    Returns:
        A four-item tuple of integers representing the bounding rectangle:
        ``(xMin, yMin, xMax, yMax)``.
    """
    return tuple(round(v) for v in calcBounds(array))

