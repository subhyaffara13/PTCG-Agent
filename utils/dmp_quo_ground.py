
def dmp_quo_ground(f, c, u, K):
    """
    Quotient by a constant in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ, QQ

    >>> R, x,y = ring("x,y", ZZ)
    >>> R.dmp_quo_ground(2*x**2*y + 3*x, ZZ(2))
    x**2*y + x

    >>> R, x,y = ring("x,y", QQ)
    >>> R.dmp_quo_ground(2*x**2*y + 3*x, QQ(2))
    x**2*y + 3/2*x

    """
    if not u:
        return dup_quo_ground(f, c, K)

    v = u - 1

    return [ dmp_quo_ground(cf, c, v, K) for cf in f ]

