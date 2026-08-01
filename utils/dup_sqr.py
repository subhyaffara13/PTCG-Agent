
def dup_sqr(f, K):
    """
    Square dense polynomials in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_sqr(x**2 + 1)
    x**4 + 2*x**2 + 1

    """
    df, h = len(f) - 1, []

    for i in range(0, 2*df + 1):
        c = K.zero

        jmin = max(0, i - df)
        jmax = min(i, df)

        n = jmax - jmin + 1

        jmax = jmin + n // 2 - 1

        for j in range(jmin, jmax + 1):
            c += f[j]*f[i - j]

        c += c

        if n & 1:
            elem = f[jmax + 1]
            c += elem**2

        h.append(c)

    return dup_strip(h)

