
def translate_vec_create_from_iterable(
    builder: IRBuilder, vec_type: RVec, arg: Expression, *, capacity: Value | None = None
) -> Value:
    line = arg.line
    item_type = vec_type.item_type
    if isinstance(arg, OpExpr) and arg.op == "*":
        if isinstance(arg.left, ListExpr):
            lst = arg.left
            other = arg.right
        elif isinstance(arg.right, ListExpr):
            lst = arg.right
            other = arg.left
        else:
            assert False
        assert len(lst.items) == 1
        other_type = builder.node_type(other)
        # TODO: is_any_int(...)
        if is_int64_rprimitive(other_type) or is_int_rprimitive(other_type):
            length = builder.accept(other)
            init = builder.accept(lst.items[0])
            return vec_create_initialized(
                builder.builder, vec_type, length, init, line, capacity=capacity
            )
        assert False, other_type
    if isinstance(arg, ListExpr):
        items = []
        for item in arg.items:
            value = builder.accept(item)
            items.append(builder.coerce(value, item_type, line))
        return vec_create_from_values(builder.builder, vec_type, items, line, capacity=capacity)
    if isinstance(arg, ListComprehension):
        return translate_vec_comprehension(builder, vec_type, arg.generator, capacity=capacity)
    return vec_from_iterable(builder, vec_type, arg, line, capacity=capacity)

