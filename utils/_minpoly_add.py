
def _minpoly_add(x, dom, *a):
    """
    returns ``minpoly(Add(*a), dom, x)``
    """
    mp = _minpoly_op_algebraic_element(Add, a[0], a[1], x, dom)
    p = a[0] + a[1]
    for px in a[2:]:
        mp = _minpoly_op_algebraic_element(Add, p, px, x, dom, mp1=mp)
        p = p + px
    return mp

