
def as_symbol(obj):
    """Return object as SYMBOL expression (variable or unparsed expression).
    """
    return Expr(Op.SYMBOL, obj)

