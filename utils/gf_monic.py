
def gf_monic(f, p, K):
    """
    Compute LC and a monic polynomial in ``GF(p)[x]``.

    Examples
    ========

    >>> from sympy.polys.domains import ZZ
    >>> from sympy.polys.galoistools import gf_monic

    >>> gf_monic(ZZ.map([3, 2, 4]), 5, ZZ)
    (3, [1, 4, 3])

    """
    if not f:
        return K.zero, []
    else:
        lc = f[0]

        if K.is_one(lc):
            return lc, list(f)
        else:
            return lc, gf_quo_ground(f, lc, p, K)

