
def as_terms(obj):
    """Return expression as TERMS expression.
    """
    if isinstance(obj, Expr):
        obj = normalize(obj)
        if obj.op is Op.TERMS:
            return obj
        if obj.op is Op.INTEGER:
            return Expr(Op.TERMS, {as_integer(1, obj.data[1]): obj.data[0]})
        if obj.op is Op.REAL:
            return Expr(Op.TERMS, {as_real(1, obj.data[1]): obj.data[0]})
        return Expr(Op.TERMS, {obj: 1})
    raise OpError(f'cannot convert {type(obj)} to terms Expr')

