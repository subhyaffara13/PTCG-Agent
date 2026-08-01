
def dmp_normal(f, u, K):
    """
    Normalize a multivariate polynomial in the given domain.

    Examples
    ========

    >>> from sympy.polys.domains import ZZ
    >>> from sympy.polys.densebasic import dmp_normal

    >>> dmp_normal([[], [0, 1, 2]], 1, ZZ)
    [[1, 2]]

    """
    if not u:
        return dup_normal(f, K)

    v = u - 1

    return dmp_strip([ dmp_normal(c, v, K) for c in f ], u)

