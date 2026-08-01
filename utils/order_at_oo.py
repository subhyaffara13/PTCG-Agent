
def order_at_oo(a, d, t):
    """
    Computes the order of a/d at oo (infinity), with respect to t.

    For f in k(t), the order or f at oo is defined as deg(d) - deg(a), where
    f == a/d.
    """
    if a.is_zero:
        return oo
    return d.degree(t) - a.degree(t)

