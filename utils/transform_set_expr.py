
def transform_set_expr(builder: IRBuilder, expr: SetExpr) -> Value:
    return _visit_display(
        builder, expr.items, builder.new_set_op, set_add_op, set_update_op, expr.line, False
    )

