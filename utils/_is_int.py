
def _is_int(expr: object) -> TypeGuard[SymInt]:
    return isinstance(expr, SymInt) and expr.node.expr.is_number

