
def dmp_max_norm(f, u, K):
    """
    Returns maximum norm of a polynomial in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_max_norm(2*x*y - x - 3)
    3

    """
    if not u:
        return dup_max_norm(f, K)

    v = u - 1

    return max(dmp_max_norm(c, v, K) for c in f)

