
def as_eq(left, right):
    return Expr(Op.RELATIONAL, (RelOp.EQ, left, right))

