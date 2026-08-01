
def as_integer(obj, kind=4):
    """Return object as INTEGER constant.
    """
    if isinstance(obj, int):
        return Expr(Op.INTEGER, (obj, kind))
    if isinstance(obj, Expr):
        if obj.op is Op.INTEGER:
            return obj
    raise OpError(f'cannot convert {obj} to INTEGER constant')

