
def try_constant_fold(builder: IRBuilder, expr: Expression) -> Value | None:
    """Return the constant value of an expression if possible.

    Return None otherwise.
    """
    value = constant_fold_expr(builder, expr)
    if value is not None:
        return builder.load_literal_value(value)
    return None

