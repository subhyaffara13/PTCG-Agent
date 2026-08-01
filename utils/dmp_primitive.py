
def dmp_primitive(f, u, K):
    """
    Returns multivariate content and a primitive polynomial.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y, = ring("x,y", ZZ)

    >>> R.dmp_primitive(2*x*y + 6*x + 4*y + 12)
    (2*y + 6, x + 2)

    """
    cont, v = dmp_content(f, u, K), u - 1

    if dmp_zero_p(f, u) or dmp_one_p(cont, v, K):
        return cont, f
    else:
        return cont, [ dmp_quo(c, cont, v, K) for c in f ]

