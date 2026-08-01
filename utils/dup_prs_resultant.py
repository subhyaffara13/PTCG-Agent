
def dup_prs_resultant(f, g, K):
    """
    Resultant algorithm in `K[x]` using subresultant PRS.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_prs_resultant(x**2 + 1, x**2 - 1)
    (4, [x**2 + 1, x**2 - 1, -2])

    """
    if not f or not g:
        return (K.zero, [])

    R, S = dup_inner_subresultants(f, g, K)

    if dup_degree(R[-1]) > 0:
        return (K.zero, R)

    return S[-1], R

