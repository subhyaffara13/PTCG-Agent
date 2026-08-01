
def roots_linear(f):
    """Returns a list of roots of a linear polynomial."""
    r = -f.nth(0)/f.nth(1)
    dom = f.get_domain()

    if not dom.is_Numerical:
        if dom.is_Composite:
            r = factor(r)
        else:
            from sympy.simplify.simplify import simplify
            r = simplify(r)

    return [r]

