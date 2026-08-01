
def dmp_abs(f, u, K):
    """
    Make all coefficients positive in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_abs(x**2*y - x)
    x**2*y + x

    """
    if not u:
        return dup_abs(f, K)

    v = u - 1

    return [ dmp_abs(cf, v, K) for cf in f ]

