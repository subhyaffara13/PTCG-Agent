
def try_gen_slice_op(builder: IRBuilder, base: Value, index: SliceExpr) -> Value | None:
    """Generate specialized slice op for some index expressions.

    Return None if a specialized op isn't available.

    This supports obj[x:y], obj[:x], and obj[x:] for a few types.
    """
    if index.stride:
        # We can only handle the default stride of 1.
        return None

    if index.begin_index:
        begin_type = builder.node_type(index.begin_index)
    else:
        begin_type = int_rprimitive
    if index.end_index:
        end_type = builder.node_type(index.end_index)
    else:
        end_type = int_rprimitive

    # Both begin and end index must be int (or missing).
    if is_any_int(begin_type) and is_any_int(end_type):
        if index.begin_index:
            begin = builder.accept(index.begin_index)
        else:
            begin = builder.load_int(0)
        if index.end_index:
            end = builder.accept(index.end_index)
        else:
            # Replace missing end index with the largest short integer
            # (a sequence can't be longer).
            end = builder.load_int(MAX_SHORT_INT)
        if isinstance(base.type, RVec):
            return vec_slice(builder.builder, base, begin, end, index.line)
        candidates = [list_slice_op, tuple_slice_op, str_slice_op, bytes_slice_op]
        return builder.builder.matching_call_c(candidates, [base, begin, end], index.line)

    return None

