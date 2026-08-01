
def gf_mul_ground(f, a, p, K):
    """
    Compute ``f * a`` where ``f`` in ``GF(p)[x]`` and ``a`` in ``GF(p)``.

    Examples
    ========

    >>> from sympy.polys.domains import ZZ
    >>> from sympy.polys.galoistools import gf_mul_ground

    >>> gf_mul_ground([3, 2, 4], 2, 5, ZZ)
    [1, 4, 3]

    """
    if not a:
        return []
    else:
        return [ (a*b) % p for b in f ]

