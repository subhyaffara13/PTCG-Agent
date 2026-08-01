
def translate_refexpr_call(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value:
    """Translate a non-method call."""
    # Gen the argument values
    arg_values = [builder.accept(arg) for arg in expr.args]

    return builder.call_refexpr_with_args(expr, callee, arg_values)

