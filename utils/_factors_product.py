
def _factors_product(factors):
    """Multiply a list of ``(expr, exp)`` pairs. """
    return Mul(*[f.as_expr()**k for f, k in factors])

