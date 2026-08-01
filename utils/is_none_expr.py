
def is_none_expr(expr: Expression) -> bool:
    return isinstance(expr, NameExpr) and expr.name == "None"

