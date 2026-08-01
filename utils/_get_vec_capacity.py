
def _get_vec_capacity(builder: IRBuilder, expr: CallExpr) -> Value | None:
    """Extract the 'capacity' keyword argument value from a vec() call, or None."""
    for i, (kind, name) in enumerate(zip(expr.arg_kinds, expr.arg_names)):
        if kind == ARG_NAMED and name == "capacity":
            return builder.accept(expr.args[i])
    return None

