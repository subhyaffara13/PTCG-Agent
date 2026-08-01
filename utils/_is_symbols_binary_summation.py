
def _is_symbols_binary_summation(expr: sympy.Expr) -> bool:
    # No need to check that two args are not the same, since expr is pr-optimized but we do it anyway.
    return (
        isinstance(expr, sympy.Expr)
        and expr.is_Add
        and len(expr._args) == 2
        and expr._args[0].is_symbol
        and expr._args[1].is_symbol
        and expr._args[0] is not expr._args[1]
    )

