
def _minpoly_mul(x, dom, *a):
    """
    returns ``minpoly(Mul(*a), dom, x)``
    """
    mp = _minpoly_op_algebraic_element(Mul, a[0], a[1], x, dom)
    p = a[0] * a[1]
    for px in a[2:]:
        mp = _minpoly_op_algebraic_element(Mul, p, px, x, dom, mp1=mp)
        p = p * px
    return mp

