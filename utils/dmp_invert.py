
def dmp_invert(f, g, u, K):
    """
    Compute multiplicative inverse of `f` modulo `g` in `F[X]`.

    Examples
    ========

    >>> from sympy.polys import ring, QQ
    >>> R, x = ring("x", QQ)

    """
    if not u:
        return dup_invert(f, g, K)
    else:
        raise MultivariatePolynomialError(f, g)

