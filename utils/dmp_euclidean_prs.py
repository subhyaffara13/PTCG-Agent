
def dmp_euclidean_prs(f, g, u, K):
    """
    Euclidean polynomial remainder sequence (PRS) in `K[X]`.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    """
    if not u:
        return dup_euclidean_prs(f, g, K)
    else:
        raise MultivariatePolynomialError(f, g)

