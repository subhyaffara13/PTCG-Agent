
def dmp_l2_norm_squared(f, u, K):
    """
    Returns squared l2 norm of a polynomial in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_l2_norm_squared(2*x*y - x - 3)
    14

    """
    if not u:
        return dup_l2_norm_squared(f, K)

    v = u - 1

    return sum(dmp_l2_norm_squared(c, v, K) for c in f)

