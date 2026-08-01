
def dmp_pdiv(f, g, u, K):
    """
    Polynomial pseudo-division in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_pdiv(x**2 + x*y, 2*x + 2)
    (2*x + 2*y - 2, -4*y + 4)

    """
    if not u:
        return dup_pdiv(f, g, K)

    df = dmp_degree(f, u)
    dg = dmp_degree(g, u)

    if dg < 0:
        raise ZeroDivisionError("polynomial division")

    q, r, dr = dmp_zero(u), f, df

    if df < dg:
        return q, r

    N = df - dg + 1
    lc_g = dmp_LC(g, K)

    while True:
        lc_r = dmp_LC(r, K)
        j, N = dr - dg, N - 1

        Q = dmp_mul_term(q, lc_g, 0, u, K)
        q = dmp_add_term(Q, lc_r, j, u, K)

        R = dmp_mul_term(r, lc_g, 0, u, K)
        G = dmp_mul_term(g, lc_r, j, u, K)
        r = dmp_sub(R, G, u, K)

        _dr, dr = dr, dmp_degree(r, u)

        if dr < dg:
            break
        elif not (dr < _dr):
            raise PolynomialDivisionFailed(f, g, K)

    c = dmp_pow(lc_g, N, u - 1, K)

    q = dmp_mul_term(q, c, 0, u, K)
    r = dmp_mul_term(r, c, 0, u, K)

    return q, r

