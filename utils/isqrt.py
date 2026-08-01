
def isqrt(n):
    r""" Return the largest integer less than or equal to `\sqrt{n}`.

    Parameters
    ==========

    n : non-negative integer

    Returns
    =======

    int : `\left\lfloor\sqrt{n}\right\rfloor`

    Raises
    ======

    ValueError
        If n is negative.
    TypeError
        If n is of a type that cannot be compared to ``int``.
        Therefore, a TypeError is raised for ``str``, but not for ``float``.

    Examples
    ========

    >>> from sympy.core.intfunc import isqrt
    >>> isqrt(0)
    0
    >>> isqrt(9)
    3
    >>> isqrt(10)
    3
    >>> isqrt("30")
    Traceback (most recent call last):
        ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    >>> from sympy.core.numbers import Rational
    >>> isqrt(Rational(-1, 2))
    Traceback (most recent call last):
        ...
    ValueError: n must be nonnegative

    """
    if n < 0:
        raise ValueError("n must be nonnegative")
    return int(sqrt(int(n)))

