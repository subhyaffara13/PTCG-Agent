
def dmp_l1_norm(f, u, K):
    """
    Returns l1 norm of a polynomial in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_l1_norm(2*x*y - x - 3)
    6

    """
    if not u:
        return dup_l1_norm(f, K)

    v = u - 1

    return sum(dmp_l1_norm(c, v, K) for c in f)

