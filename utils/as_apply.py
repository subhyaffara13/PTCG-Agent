
def as_apply(func, *args, **kwargs):
    """Return object as APPLY expression (function call, constructor, etc.)
    """
    return Expr(Op.APPLY,
                (func, tuple(map(as_expr, args)),
                 {k: as_expr(v) for k, v in kwargs.items()}))

