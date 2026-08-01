
def dup_pow(f, n, K):
    """
    Raise ``f`` to the ``n``-th power in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_pow(x - 2, 3)
    x**3 - 6*x**2 + 12*x - 8

    """
    if not n:
        return [K.one]
    if n < 0:
        raise ValueError("Cannot raise polynomial to a negative power")
    if n == 1 or not f or f == [K.one]:
        return f

    g = [K.one]

    while True:
        n, m = n//2, n

        if m % 2:
            g = dup_mul(g, f, K)

            if not n:
                break

        f = dup_sqr(f, K)

    return g

