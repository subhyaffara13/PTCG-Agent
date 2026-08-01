
def transform_index_expr(builder: IRBuilder, expr: IndexExpr) -> Value:
    index = expr.index
    base_type = builder.node_type(expr.base)
    # We can borrow a list item safely only if GIL is enabled. The vec type is optimized for
    # performance, so we'll do unsafe borrowing.
    can_borrow = (is_list_rprimitive(base_type) and not IS_FREE_THREADED) or isinstance(
        base_type, RVec
    )
    can_borrow_base = (
        is_list_rprimitive(base_type) or isinstance(base_type, RVec)
    ) and is_borrow_friendly_expr(builder, index)

    # Check for dunder specialization for non-slice indexing
    if not isinstance(index, SliceExpr):
        specialized = apply_dunder_specialization(builder, expr.base, [index], "__getitem__", expr)
        if specialized is not None:
            return specialized

    base = builder.accept(expr.base, can_borrow=can_borrow_base)

    if isinstance(base.type, RTuple):
        folded_index = constant_fold_expr(builder, index)
        if isinstance(folded_index, int):
            length = len(base.type.types)
            if -length <= folded_index <= length - 1:
                return builder.add(TupleGet(base, folded_index, expr.line))

    if isinstance(index, SliceExpr):
        value = try_gen_slice_op(builder, base, index)
        if value:
            return value

    index_reg = builder.accept(expr.index, can_borrow=can_borrow or can_borrow_base)
    return builder.builder.get_item(
        base, index_reg, builder.node_type(expr), expr.line, can_borrow=builder.can_borrow
    )

