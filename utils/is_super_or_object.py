
def is_super_or_object(expr: CallExpr, callee: RefExpr) -> bool:
    """Returns True for super().<name> or object.<name> calls."""
    return isinstance(expr.callee, SuperExpr) or is_object(callee)

