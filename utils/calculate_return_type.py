
def calculate_return_type(expr: Expression) -> ProperType | None:
    """Return the return type if we can calculate it.

    This only uses information available during semantic analysis so this
    will sometimes return None because of insufficient information (as
    type inference hasn't run yet).
    """
    if isinstance(expr, RefExpr):
        if isinstance(expr.node, FuncDef):
            typ = expr.node.type
            if typ is None:
                # No signature -> default to Any.
                return AnyType(TypeOfAny.unannotated)
            # Explicit Any return?
            if isinstance(typ, CallableType):
                return get_proper_type(typ.ret_type)
            return None
        elif isinstance(expr.node, Var):
            return get_proper_type(expr.node.type)
    elif isinstance(expr, CallExpr):
        return calculate_return_type(expr.callee)
    return None

