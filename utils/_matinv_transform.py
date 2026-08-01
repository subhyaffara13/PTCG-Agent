
def _matinv_transform(expr):
    left, right = expr.args
    inv_arg = left.arg
    return MatrixSolve(inv_arg, right)

