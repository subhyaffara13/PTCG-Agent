
def translate_call(builder: IRBuilder, expr: CallExpr, callee: Expression) -> Value:
    # The common case of calls is refexprs
    if isinstance(callee, RefExpr):
        return apply_function_specialization(builder, expr, callee) or translate_refexpr_call(
            builder, expr, callee
        )

    function = builder.accept(callee)
    args = [builder.accept(arg) for arg in expr.args]
    return builder.py_call(
        function, args, expr.line, arg_kinds=expr.arg_kinds, arg_names=expr.arg_names
    )

