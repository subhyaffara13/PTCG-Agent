
def dmp_sub_term(f, c, i, u, K):
    """
    Subtract ``c(x_2..x_u)*x_0**i`` from ``f`` in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_sub_term(2*x**2 + x*y + 1, 2, 2)
    x*y + 1

    """
    if not u:
        return dup_add_term(f, -c, i, K)

    v = u - 1

    if dmp_zero_p(c, v):
        return f

    n = len(f)
    m = n - i - 1

    if i == n - 1:
        return dmp_strip([dmp_sub(f[0], c, v, K)] + f[1:], u)
    else:
        if i >= n:
            return [dmp_neg(c, v, K)] + dmp_zeros(i - n, v, K) + f
        else:
            return f[:m] + [dmp_sub(f[m], c, v, K)] + f[m + 1:]

