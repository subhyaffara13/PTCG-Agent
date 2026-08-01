
def as_string(obj, kind=1):
    """Return object as STRING expression (string literal constant).
    """
    return Expr(Op.STRING, (obj, kind))

