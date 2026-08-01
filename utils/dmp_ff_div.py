
def dmp_ff_div(f, g, u, K):
    """
    Polynomial division with remainder over a field.

    Examples
    ========

    >>> from sympy.polys import ring, QQ
    >>> R, x,y = ring("x,y", QQ)

    >>> R.dmp_ff_div(x**2 + x*y, 2*x + 2)
    (1/2*x + 1/2*y - 1/2, -y + 1)

    """
    if not u:
        return dup_ff_div(f, g, K)

    df = dmp_degree(f, u)
    dg = dmp_degree(g, u)

    if dg < 0:
        raise ZeroDivisionError("polynomial division")

    q, r, dr = dmp_zero(u), f, df

    if df < dg:
        return q, r

    lc_g, v = dmp_LC(g, K), u - 1

    while True:
        lc_r = dmp_LC(r, K)
        c, R = dmp_ff_div(lc_r, lc_g, v, K)

        if not dmp_zero_p(R, v):
            break

        j = dr - dg

        q = dmp_add_term(q, c, j, u, K)
        h = dmp_mul_term(g, c, j, u, K)
        r = dmp_sub(r, h, u, K)

        _dr, dr = dr, dmp_degree(r, u)

        if dr < dg:
            break
        elif not (dr < _dr):
            raise PolynomialDivisionFailed(f, g, K)

    return q, r

