
def dotproduct(vec1, vec2):
    """Returns the dot product of the two iterables.

    >>> dotproduct([10, 15, 12], [0.65, 0.80, 1.25])
    33.5
    >>> 10 * 0.65 + 15 * 0.80 + 12 * 1.25
    33.5

    In Python 3.12 and later, use ``math.sumprod()`` instead.
    """
    return sum(map(mul, vec1, vec2))

