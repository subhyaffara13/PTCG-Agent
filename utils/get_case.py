
def get_case(d, t):
    """
    Returns the type of the derivation d.

    Returns one of {'exp', 'tan', 'base', 'primitive', 'other_linear',
    'other_nonlinear'}.
    """
    if not d.expr.has(t):
        if d.is_one:
            return 'base'
        return 'primitive'
    if d.rem(Poly(t, t)).is_zero:
        return 'exp'
    if d.rem(Poly(1 + t**2, t)).is_zero:
        return 'tan'
    if d.degree(t) > 1:
        return 'other_nonlinear'
    return 'other_linear'

