
def dmp_alg_inject(f, u, K):
    """
    Convert polynomial from ``K(a)[X]`` to ``K[a,X]``.

    Examples
    ========

    >>> from sympy.polys.densetools import dmp_alg_inject
    >>> from sympy import QQ, sqrt

    >>> K = QQ.algebraic_field(sqrt(2))

    >>> p = [K.from_sympy(sqrt(2)), K.zero, K.one]
    >>> P, lev, dom = dmp_alg_inject(p, 0, K)
    >>> P
    [[1, 0, 0], [1]]
    >>> lev
    1
    >>> dom
    QQ

    """
    if K.is_GaussianRing or K.is_GaussianField:
        return _dmp_alg_inject_gaussian(f, u, K)
    elif K.is_Algebraic:
        return _dmp_alg_inject_alg(f, u, K)
    else:
        raise DomainError('computation can be done only in an algebraic domain')

