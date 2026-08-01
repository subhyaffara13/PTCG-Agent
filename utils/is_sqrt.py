
def is_sqrt(expr):
    """Return True if expr is a sqrt, otherwise False."""

    return expr.is_Pow and expr.exp.is_Rational and abs(expr.exp) is S.Half

