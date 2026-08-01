
def dmp_add(f, g, u, K):
    """
    Add dense polynomials in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_add(x**2 + y, x**2*y + x)
    x**2*y + x**2 + x + y

    """
    if not u:
        return dup_add(f, g, K)

    df = dmp_degree(f, u)

    if df < 0:
        return g

    dg = dmp_degree(g, u)

    if dg < 0:
        return f

    v = u - 1

    if df == dg:
        return dmp_strip([ dmp_add(a, b, v, K) for a, b in zip(f, g) ], u)
    else:
        k = abs(df - dg)

        if df > dg:
            h, f = f[:k], f[k:]
        else:
            h, g = g[:k], g[k:]

        return h + [ dmp_add(a, b, v, K) for a, b in zip(f, g) ]

