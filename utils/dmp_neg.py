
def dmp_neg(f, u, K):
    """
    Negate a polynomial in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_neg(x**2*y - x)
    -x**2*y + x

    """
    if not u:
        return dup_neg(f, K)

    v = u - 1

    return [ dmp_neg(cf, v, K) for cf in f ]

