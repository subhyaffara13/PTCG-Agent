
def dup_rem(f, g, K):
    """
    Returns polynomial remainder in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ, QQ

    >>> R, x = ring("x", ZZ)
    >>> R.dup_rem(x**2 + 1, 2*x - 4)
    x**2 + 1

    >>> R, x = ring("x", QQ)
    >>> R.dup_rem(x**2 + 1, 2*x - 4)
    5

    """
    return dup_div(f, g, K)[1]

