
def gf_add_ground(f, a, p, K):
    """
    Compute ``f + a`` where ``f`` in ``GF(p)[x]`` and ``a`` in ``GF(p)``.

    Examples
    ========

    >>> from sympy.polys.domains import ZZ
    >>> from sympy.polys.galoistools import gf_add_ground

    >>> gf_add_ground([3, 2, 4], 2, 5, ZZ)
    [3, 2, 1]

    """
    if not f:
        a = a % p
    else:
        a = (f[-1] + a) % p

        if len(f) > 1:
            return f[:-1] + [a]

    if not a:
        return []
    else:
        return [a]

