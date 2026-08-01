
def dup_compose(f, g, K):
    """
    Evaluate functional composition ``f(g)`` in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_compose(x**2 + x, x - 1)
    x**2 - x

    """
    if len(g) <= 1:
        return dup_strip([dup_eval(f, dup_LC(g, K), K)])

    if not f:
        return []

    h = [f[0]]

    for c in f[1:]:
        h = dup_mul(h, g, K)
        h = dup_add_term(h, c, 0, K)

    return h

