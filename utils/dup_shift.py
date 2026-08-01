
def dup_shift(f, a, K):
    """
    Evaluate efficiently Taylor shift ``f(x + a)`` in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_shift(x**2 - 2*x + 1, ZZ(2))
    x**2 + 2*x + 1

    """
    f, n = list(f), len(f) - 1

    for i in range(n, 0, -1):
        for j in range(0, i):
            f[j + 1] += a*f[j]

    return f

