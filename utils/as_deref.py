
def as_deref(expr):
    """Return object as dereferencing expression.
    """
    return Expr(Op.DEREF, expr)

