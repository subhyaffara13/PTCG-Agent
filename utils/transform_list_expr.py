
def transform_list_expr(builder: IRBuilder, expr: ListExpr) -> Value:
    return _visit_list_display(builder, expr.items, expr.line)

