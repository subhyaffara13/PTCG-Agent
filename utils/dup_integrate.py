
def dup_integrate(f, m, K):
    """
    Computes the indefinite integral of ``f`` in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, QQ
    >>> R, x = ring("x", QQ)

    >>> R.dup_integrate(x**2 + 2*x, 1)
    1/3*x**3 + x**2
    >>> R.dup_integrate(x**2 + 2*x, 2)
    1/12*x**4 + 1/3*x**3

    """
    if m <= 0 or not f:
        return f

    g = [K.zero]*m

    for i, c in enumerate(reversed(f)):
        n = i + 1

        for j in range(1, m):
            n *= i + j + 1

        g.insert(0, K.exquo(c, K(n)))

    return g

