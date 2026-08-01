
def find_fixed_callable_return(expr: Expression) -> CallableType | None:
    """Return the return type, if expression refers to a callable that returns a callable.

    But only do this if the return type has no type variables. Return None otherwise.
    This approximates things a lot as this is supposed to be called before type checking
    when full type information is not available yet.
    """
    if isinstance(expr, RefExpr):
        if isinstance(expr.node, FuncDef):
            typ = expr.node.type
            if typ:
                if isinstance(typ, CallableType) and has_no_typevars(typ.ret_type):
                    ret_type = get_proper_type(typ.ret_type)
                    if isinstance(ret_type, CallableType):
                        return ret_type
    elif isinstance(expr, CallExpr):
        t = find_fixed_callable_return(expr.callee)
        if t:
            ret_type = get_proper_type(t.ret_type)
            if isinstance(ret_type, CallableType):
                return ret_type
    return None

