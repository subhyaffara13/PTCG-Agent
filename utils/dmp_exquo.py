
def dmp_exquo(f, g, u, K):
    """
    Returns polynomial quotient in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> f = x**2 + x*y
    >>> g = x + y
    >>> h = 2*x + 2

    >>> R.dmp_exquo(f, g)
    x

    >>> R.dmp_exquo(f, h)
    Traceback (most recent call last):
    ...
    ExactQuotientFailed: [[2], [2]] does not divide [[1], [1, 0], []]

    """
    q, r = dmp_div(f, g, u, K)

    if dmp_zero_p(r, u):
        return q
    else:
        raise ExactQuotientFailed(f, g)

