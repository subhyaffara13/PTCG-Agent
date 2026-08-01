
def _matinv_predicate(expr):
    # TODO: We should be able to support more than 2 elements
    if expr.is_MatMul and len(expr.args) == 2:
        left, right = expr.args
        if left.is_Inverse and right.shape[1] == 1:
            inv_arg = left.arg
            if isinstance(inv_arg, MatrixSymbol):
                return bool(ask(Q.fullrank(left.arg)))

    return False

