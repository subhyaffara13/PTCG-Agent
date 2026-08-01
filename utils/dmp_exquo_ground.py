
def dmp_exquo_ground(f, c, u, K):
    """
    Exact quotient by a constant in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, QQ
    >>> R, x,y = ring("x,y", QQ)

    >>> R.dmp_exquo_ground(x**2*y + 2*x, QQ(2))
    1/2*x**2*y + x

    """
    if not u:
        return dup_exquo_ground(f, c, K)

    v = u - 1

    return [ dmp_exquo_ground(cf, c, v, K) for cf in f ]

