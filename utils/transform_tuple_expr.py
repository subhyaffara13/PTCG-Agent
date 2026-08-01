
def transform_tuple_expr(builder: IRBuilder, expr: TupleExpr) -> Value:
    if any(isinstance(item, StarExpr) for item in expr.items):
        # create a tuple of unknown length
        return _visit_tuple_display(builder, expr)

    # create a tuple of fixed length (RTuple)
    tuple_type = builder.node_type(expr)
    # When handling NamedTuple et. al we might not have proper type info,
    # so make some up if we need it.
    types = (
        tuple_type.types
        if isinstance(tuple_type, RTuple)
        else [object_rprimitive] * len(expr.items)
    )

    items = []
    for item_expr, item_type in zip(expr.items, types):
        reg = builder.accept(item_expr)
        item = builder.coerce(reg, item_type, item_expr.line)
        if isinstance(item, Register):
            temp = Register(item.type)
            builder.assign(temp, item, item_expr.line)
            item = temp
        items.append(item)
    return builder.add(TupleSet(items, expr.line))

