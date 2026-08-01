
def is_constant(x):
    values = x.values.ravel("K")
    return len(set(values[notna(values)])) == 1


def is_constant(e: Expression) -> bool:
    """Check whether we allow an expression to appear as a default value.

    We don't currently properly support storing the evaluated
    values for default arguments and default attribute values, so
    we restrict what expressions we allow.  We allow literals of
    primitives types, None, and references to Final global
    variables.
    """
    return (
        isinstance(e, (StrExpr, BytesExpr, IntExpr, FloatExpr))
        or (isinstance(e, UnaryExpr) and e.op == "-" and isinstance(e.expr, (IntExpr, FloatExpr)))
        or (isinstance(e, TupleExpr) and all(is_constant(e) for e in e.items))
        or (
            isinstance(e, RefExpr)
            and e.kind == GDEF
            and (
                e.fullname in ("builtins.True", "builtins.False", "builtins.None")
                or (isinstance(e.node, Var) and e.node.is_final)
            )
        )
    )

