
def dmp_degree_list(f, u):
    """
    Return a list of degrees of ``f`` in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys.domains import ZZ
    >>> from sympy.polys.densebasic import dmp_degree_list

    >>> f = ZZ.map([[1], [1, 2, 3]])

    >>> dmp_degree_list(f, 1)
    (1, 2)

    """
    degs = [ninf]*(u + 1)
    _rec_degree_list(f, u, 0, degs)
    return tuple(degs)

