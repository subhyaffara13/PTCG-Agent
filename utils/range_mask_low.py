
def range_mask_low(i: sympy.Expr, low: sympy.Expr | int):
    return ops.ge(
        ops.index_expr(i, torch.int64),
        ops.index_expr(sympy.Integer(low), torch.int64),
    )

