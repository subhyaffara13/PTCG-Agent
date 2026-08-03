import functools

def argsort_sym(
    shape_env: ShapeEnv,
    seq: Sequence[int | torch.SymInt | sympy.Expr],
    *,
    reverse: bool = False,
) -> list[int]:
    def cmp(a: tuple[int, sympy.Expr], b: tuple[int, sympy.Expr]) -> int:
        a_idx, a_val = a
        b_idx, b_val = b

        def evaluate(expr: bool | torch.SymInt | sympy.Expr) -> bool:
            if isinstance(expr, bool):
                return expr
            return shape_env.evaluate_expr(expr, size_oblivious=True)

        if evaluate(a_val < b_val):
            return -1
        if evaluate(a_val > b_val):
            return 1
        # If strides are the same, prefer the original order.
        # (this matches argsort's algorithm).
        # For strides = [2048, 2048, 16, 1], this is
        # [3, 2, 1, 0].
        if a_idx < b_idx:
            return 1
        if a_idx > b_idx:
            return -1
        return 0

    # Strategy: convert all symints to sympy.Expr, then use a custom comparator
    exprs = [
        (idx, s.node.expr if isinstance(s, torch.SymInt) else s)
        for idx, s in enumerate(seq)
    ]
    exprs = sorted(exprs, key=functools.cmp_to_key(cmp), reverse=reverse)
    result = [idx for idx, _ in exprs]
    return result

