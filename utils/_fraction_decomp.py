
def _fraction_decomp(expr):
    """Return num, den such that expr = num/den."""
    if not isinstance(expr, Mul):
        return expr, 1
    num = []
    den = []
    for a in expr.args:
        if a.is_Pow and a.args[1] < 0:
            den.append(1 / a)
        else:
            num.append(a)
    if not den:
        return expr, 1
    num = Mul(*num)
    den = Mul(*den)
    return num, den

