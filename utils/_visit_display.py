
def _visit_display(
    builder: IRBuilder,
    items: list[Expression],
    constructor_op: Callable[[list[Value], int], Value],
    append_op: PrimitiveDescription,
    extend_op: PrimitiveDescription,
    line: int,
    is_list: bool,
) -> Value:
    accepted_items = []
    for item in items:
        if isinstance(item, StarExpr):
            accepted_items.append((True, builder.accept(item.expr)))
        else:
            accepted_items.append((False, builder.accept(item)))

    result: Value | None = None
    initial_items = []
    for starred, value in accepted_items:
        if result is None and not starred and is_list:
            initial_items.append(value)
            continue

        if result is None:
            result = constructor_op(initial_items, line)

        builder.primitive_op(extend_op if starred else append_op, [result, value], line)

    if result is None:
        result = constructor_op(initial_items, line)

    return result

