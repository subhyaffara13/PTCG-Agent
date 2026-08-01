
def as_lt(left, right):
    return Expr(Op.RELATIONAL, (RelOp.LT, left, right))

