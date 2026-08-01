
def _invertx(p, x):
    """
    Returns ``expand_mul(x**degree(p, x)*p.subs(x, 1/x))``
    """
    p1 = poly_from_expr(p, x)[0]

    n = degree(p1)
    a = [c * x**(n - i) for (i,), c in p1.terms()]
    return Add(*a)

