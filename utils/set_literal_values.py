
def set_literal_values(builder: IRBuilder, items: Sequence[Expression]) -> list[object] | None:
    values: list[object] = []
    for item in items:
        const_value = constant_fold_expr(builder, item)
        if const_value is not None:
            values.append(const_value)
            continue

        if isinstance(item, RefExpr):
            if item.fullname == "builtins.None":
                values.append(None)
            elif item.fullname == "builtins.True":
                values.append(True)
            elif item.fullname == "builtins.False":
                values.append(False)
        elif isinstance(item, TupleExpr):
            tuple_values = set_literal_values(builder, item.items)
            if tuple_values is not None:
                values.append(tuple(tuple_values))

    if len(values) != len(items):
        # Bail if not all items can be converted into values.
        return None
    return values

