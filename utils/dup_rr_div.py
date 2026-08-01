
def dup_rr_div(f, g, K):
    """
    Univariate division with remainder over a ring.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_rr_div(x**2 + 1, 2*x - 4)
    (0, x**2 + 1)

    """
    df = dup_degree(f)
    dg = dup_degree(g)

    q, r, dr = [], f, df

    if not g:
        raise ZeroDivisionError("polynomial division")
    elif df < dg:
        return q, r

    lc_g = dup_LC(g, K)

    while True:
        lc_r = dup_LC(r, K)

        if lc_r % lc_g:
            break

        c = K.exquo(lc_r, lc_g)
        j = dr - dg

        q = dup_add_term(q, c, j, K)
        h = dup_mul_term(g, c, j, K)
        r = dup_sub(r, h, K)

        _dr, dr = dr, dup_degree(r)

        if dr < dg:
            break
        elif not (dr < _dr):
            raise PolynomialDivisionFailed(f, g, K)

    return q, r

