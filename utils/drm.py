
def drm(n, b):
    """
    Returns the multiplicative digital root of a natural number ``n`` in a given
    base ``b`` which is a single digit value obtained by an iterative process of
    multiplying digits, on each iteration using the result from the previous
    iteration to compute the digit multiplication.

    Examples
    ========

    >>> from sympy.ntheory.factor_ import drm
    >>> drm(9876, 10)
    0

    >>> drm(49, 10)
    8

    References
    ==========

    .. [1] https://mathworld.wolfram.com/MultiplicativeDigitalRoot.html

    """

    n = abs(as_int(n))
    b = as_int(b)
    if b <= 1:
        raise ValueError("Base should be an integer greater than 1")
    while n > b:
        mul = 1
        while n > 1:
            n, r = divmod(n, b)
            if r == 0:
                return 0
            mul *= r
        n = mul
    return n

