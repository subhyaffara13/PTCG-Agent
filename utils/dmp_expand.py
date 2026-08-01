
def dmp_expand(polys, u, K):
    """
    Multiply together several polynomials in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_expand([x**2 + y**2, x + 1])
    x**3 + x**2 + x*y**2 + y**2

    """
    if not polys:
        return dmp_one(u, K)

    f = polys[0]

    for g in polys[1:]:
        f = dmp_mul(f, g, u, K)

    return f

