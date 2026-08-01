
def solve_for_zero(expr: sympy.Expr) -> sympy.Expr | None:
    """
    Given an expr with a single free symbol, solve for a constant relation that would make
    this expression 0.
    """
    if expr.is_constant():
        return None
    elif isinstance(expr, FloorDiv):
        return None

    assert len(expr.free_symbols) == 1
    free_symbol = next(iter(expr.free_symbols))
    if isinstance(expr, ModularIndexing):
        out = try_solve(sympy.Eq(expr.args[0], expr.args[2]), free_symbol)
    else:
        out = try_solve(sympy.Eq(expr, 0), free_symbol)
    if not out or not out[1].is_constant():
        return None
    return out[1]

