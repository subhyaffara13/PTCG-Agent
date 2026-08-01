
def _muly(p, x, y):
    """
    Returns ``_mexpand(y**deg*p.subs({x:x / y}))``
    """
    p1 = poly_from_expr(p, x)[0]

    n = degree(p1)
    a = [c * x**i * y**(n - i) for (i,), c in p1.terms()]
    return Add(*a)

