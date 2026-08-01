
def dmp_revert(f, g, u, K):
    """
    Compute ``f**(-1)`` mod ``x**n`` using Newton iteration.

    Examples
    ========

    >>> from sympy.polys import ring, QQ
    >>> R, x,y = ring("x,y", QQ)

    """
    if not u:
        return dup_revert(f, g, K)
    else:
        raise MultivariatePolynomialError(f, g)

