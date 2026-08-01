
def get_removed_base_fullname(expr: Expression) -> str | None:
    if isinstance(expr, IndexExpr):
        expr = expr.base
    if isinstance(expr, RefExpr):
        return expr.fullname
    return None

