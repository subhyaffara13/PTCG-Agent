
def _visit_list_display(builder: IRBuilder, items: list[Expression], line: int) -> Value:
    return _visit_display(
        builder, items, builder.new_list_op, list_append_op, list_extend_op, line, True
    )

