
def _visit_tuple_display(builder: IRBuilder, expr: TupleExpr) -> Value:
    """Create a list, then turn it into a tuple."""
    val_as_list = _visit_list_display(builder, expr.items, expr.line)
    return builder.primitive_op(list_tuple_op, [val_as_list], expr.line)

