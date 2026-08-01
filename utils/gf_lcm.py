
def gf_lcm(f, g, p, K):
    """
    Compute polynomial LCM in ``GF(p)[x]``.

    Examples
    ========

    >>> from sympy.polys.domains import ZZ
    >>> from sympy.polys.galoistools import gf_lcm

    >>> gf_lcm(ZZ.map([3, 2, 4]), ZZ.map([2, 2, 3]), 5, ZZ)
    [1, 2, 0, 4]

    """
    if not f or not g:
        return []

    h = gf_quo(gf_mul(f, g, p, K),
               gf_gcd(f, g, p, K), p, K)

    return gf_monic(h, p, K)[1]

