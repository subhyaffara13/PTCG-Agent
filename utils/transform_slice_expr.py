
def transform_slice_expr(builder: IRBuilder, expr: SliceExpr) -> Value:
    def get_arg(arg: Expression | None) -> Value:
        if arg is None:
            return builder.none_object()
        else:
            return builder.accept(arg)

    args = [get_arg(expr.begin_index), get_arg(expr.end_index), get_arg(expr.stride)]
    return builder.primitive_op(new_slice_op, args, expr.line)

