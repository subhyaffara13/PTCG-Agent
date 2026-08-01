
def dmp_sub(f, g, u, K):
    """
    Subtract dense polynomials in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_sub(x**2 + y, x**2*y + x)
    -x**2*y + x**2 - x + y

    """
    if not u:
        return dup_sub(f, g, K)

    df = dmp_degree(f, u)

    if df < 0:
        return dmp_neg(g, u, K)

    dg = dmp_degree(g, u)

    if dg < 0:
        return f

    v = u - 1

    if df == dg:
        return dmp_strip([ dmp_sub(a, b, v, K) for a, b in zip(f, g) ], u)
    else:
        k = abs(df - dg)

        if df > dg:
            h, f = f[:k], f[k:]
        else:
            h, g = dmp_neg(g[:k], u, K), g[k:]

        return h + [ dmp_sub(a, b, v, K) for a, b in zip(f, g) ]

