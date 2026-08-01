
def gf_mul(f, g, p, K):
    """
    Multiply polynomials in ``GF(p)[x]``.

    Examples
    ========

    >>> from sympy.polys.domains import ZZ
    >>> from sympy.polys.galoistools import gf_mul

    >>> gf_mul([3, 2, 4], [2, 2, 2], 5, ZZ)
    [1, 0, 3, 2, 3]

    """
    df = gf_degree(f)
    dg = gf_degree(g)

    dh = df + dg
    h = [0]*(dh + 1)

    for i in range(0, dh + 1):
        coeff = K.zero

        for j in range(max(0, i - dg), min(i, df) + 1):
            coeff += f[j]*g[i - j]

        h[i] = coeff % p

    return gf_strip(h)

