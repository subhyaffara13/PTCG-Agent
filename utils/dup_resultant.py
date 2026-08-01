
def dup_resultant(f, g, K, includePRS=False):
    """
    Computes resultant of two polynomials in `K[x]`.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_resultant(x**2 + 1, x**2 - 1)
    4

    """
    if includePRS:
        return dup_prs_resultant(f, g, K)
    return dup_prs_resultant(f, g, K)[0]

