
def expand_dirac_delta(expr):
    """
    Expand an expression involving DiractDelta to get it as a linear
    combination of DiracDelta functions.
    """
    return _lin_eq2dict(expr, expr.atoms(DiracDelta))

