
def sympify_mpmath(x):
    return Expr._from_mpmath(x, x.context.prec)

