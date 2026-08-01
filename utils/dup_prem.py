
def dup_prem(f, g, K):
    """
    Polynomial pseudo-remainder in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_prem(x**2 + 1, 2*x - 4)
    20

    """
    df = dup_degree(f)
    dg = dup_degree(g)

    r, dr = f, df

    if not g:
        raise ZeroDivisionError("polynomial division")
    elif df < dg:
        return r

    N = df - dg + 1
    lc_g = dup_LC(g, K)

    while True:
        lc_r = dup_LC(r, K)
        j, N = dr - dg, N - 1

        R = dup_mul_ground(r, lc_g, K)
        G = dup_mul_term(g, lc_r, j, K)
        r = dup_sub(R, G, K)

        _dr, dr = dr, dup_degree(r)

        if dr < dg:
            break
        elif not (dr < _dr):
            raise PolynomialDivisionFailed(f, g, K)

    return dup_mul_ground(r, lc_g**N, K)

