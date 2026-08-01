
def gf_shoup(f, p, K):
    """
    Factor a square-free ``f`` in ``GF(p)[x]`` for large ``p``.

    Examples
    ========

    >>> from sympy.polys.domains import ZZ
    >>> from sympy.polys.galoistools import gf_shoup

    >>> gf_shoup(ZZ.map([1, 4, 3]), 5, ZZ)
    [[1, 1], [1, 3]]

    """
    factors = []

    for factor, n in gf_ddf_shoup(f, p, K):
        factors += gf_edf_shoup(factor, n, p, K)

    return _sort_factors(factors, multiple=False)

