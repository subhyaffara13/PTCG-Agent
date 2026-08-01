
def dup_mul_ground(f, c, K):
    """
    Multiply ``f`` by a constant value in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_mul_ground(x**2 + 2*x - 1, ZZ(3))
    3*x**2 + 6*x - 3

    """
    if not c or not f:
        return []
    else:
        return [ cf * c for cf in f ]

