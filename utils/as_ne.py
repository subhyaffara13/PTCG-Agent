
def as_ne(left, right):
    return Expr(Op.RELATIONAL, (RelOp.NE, left, right))

