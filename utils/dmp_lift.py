
def dmp_lift(f, u, K):
    """
    Convert algebraic coefficients to integers in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, QQ
    >>> from sympy import I

    >>> K = QQ.algebraic_field(I)
    >>> R, x = ring("x", K)

    >>> f = x**2 + K([QQ(1), QQ(0)])*x + K([QQ(2), QQ(0)])

    >>> R.dmp_lift(f)
    x**4 + x**2 + 4*x + 4

    """
    # Circular import. Probably dmp_lift should be moved to euclidtools
    from .euclidtools import dmp_resultant

    F, v, K2 = dmp_alg_inject(f, u, K)

    p_a = K.mod.to_list()
    P_A = dmp_include(p_a, list(range(1, v + 1)), 0, K2)

    return dmp_resultant(F, P_A, v, K2)

