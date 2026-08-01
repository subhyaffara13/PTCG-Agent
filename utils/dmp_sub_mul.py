
def dmp_sub_mul(f, g, h, u, K):
    """
    Returns ``f - g*h`` where ``f, g, h`` are in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_sub_mul(x**2 + y, x, x + 2)
    -2*x + y

    """
    return dmp_sub(f, dmp_mul(g, h, u, K), u, K)

