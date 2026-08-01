
def is_complex_expr(expr: Any) -> bool:
    return not expr.is_symbol and not expr.is_constant()

