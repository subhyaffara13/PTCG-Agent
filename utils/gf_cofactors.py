
def gf_cofactors(f, g, p, K):
    """
    Compute polynomial GCD and cofactors in ``GF(p)[x]``.

    Examples
    ========

    >>> from sympy.polys.domains import ZZ
    >>> from sympy.polys.galoistools import gf_cofactors

    >>> gf_cofactors(ZZ.map([3, 2, 4]), ZZ.map([2, 2, 3]), 5, ZZ)
    ([1, 3], [3, 3], [2, 1])

    """
    if not f and not g:
        return ([], [], [])

    h = gf_gcd(f, g, p, K)

    return (h, gf_quo(f, h, p, K),
            gf_quo(g, h, p, K))

