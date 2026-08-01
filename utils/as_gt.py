
def as_gt(left, right):
    return Expr(Op.RELATIONAL, (RelOp.GT, left, right))

