
def dup_quo_ground(f, c, K):
    """
    Quotient by a constant in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ, QQ

    >>> R, x = ring("x", ZZ)
    >>> R.dup_quo_ground(3*x**2 + 2, ZZ(2))
    x**2 + 1

    >>> R, x = ring("x", QQ)
    >>> R.dup_quo_ground(3*x**2 + 2, QQ(2))
    3/2*x**2 + 1

    """
    if not c:
        raise ZeroDivisionError('polynomial division')
    if not f:
        return f

    if K.is_Field:
        return [ K.quo(cf, c) for cf in f ]
    else:
        return [ cf // c for cf in f ]

