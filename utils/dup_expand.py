
def dup_expand(polys, K):
    """
    Multiply together several polynomials in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_expand([x**2 - 1, x, 2])
    2*x**3 - 2*x

    """
    if not polys:
        return [K.one]

    f = polys[0]

    for g in polys[1:]:
        f = dup_mul(f, g, K)

    return f

