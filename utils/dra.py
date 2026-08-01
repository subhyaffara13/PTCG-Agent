
def dra(n, b):
    """
    Returns the additive digital root of a natural number ``n`` in base ``b``
    which is a single digit value obtained by an iterative process of summing
    digits, on each iteration using the result from the previous iteration to
    compute a digit sum.

    Examples
    ========

    >>> from sympy.ntheory.factor_ import dra
    >>> dra(3110, 12)
    8

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Digital_root

    """

    num = abs(as_int(n))
    b = as_int(b)
    if b <= 1:
        raise ValueError("Base should be an integer greater than 1")

    if num == 0:
        return 0

    return (1 + (num - 1) % (b - 1))

