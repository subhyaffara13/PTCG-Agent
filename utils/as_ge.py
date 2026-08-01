
def as_ge(left, right):
    return Expr(Op.RELATIONAL, (RelOp.GE, left, right))

