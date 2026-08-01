
def dup_l2_norm_squared(f, K):
    """
    Returns squared l2 norm of a polynomial in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_l2_norm_squared(2*x**3 - 3*x**2 + 1)
    14

    """
    return sum([coeff**2 for coeff in f], K.zero)

