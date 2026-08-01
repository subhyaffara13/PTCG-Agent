
def transform_basic_comparison(
    builder: IRBuilder, op: str, left: Value, right: Value, line: int
) -> Value:
    """Transform single comparison.

    'op' must be one of these:

       '==', '!=', '<', '<=', '>', '>='
       'in', 'not in'
       'is', 'is not'
    """
    if is_fixed_width_rtype(left.type) and op in ComparisonOp.signed_ops:
        if right.type == left.type:
            if left.type.is_signed:
                op_id = ComparisonOp.signed_ops[op]
            else:
                op_id = ComparisonOp.unsigned_ops[op]
            return builder.builder.comparison_op(left, right, op_id, line)
        elif isinstance(right, Integer):
            if left.type.is_signed:
                op_id = ComparisonOp.signed_ops[op]
            else:
                op_id = ComparisonOp.unsigned_ops[op]
            return builder.builder.comparison_op(
                left, builder.coerce(right, left.type, line), op_id, line
            )
    elif (
        is_fixed_width_rtype(right.type)
        and op in ComparisonOp.signed_ops
        and isinstance(left, Integer)
    ):
        if right.type.is_signed:
            op_id = ComparisonOp.signed_ops[op]
        else:
            op_id = ComparisonOp.unsigned_ops[op]
        return builder.builder.comparison_op(
            builder.coerce(left, right.type, line), right, op_id, line
        )

    negate = False
    if op == "is not":
        op, negate = "is", True
    elif op == "not in":
        op, negate = "in", True

    target = builder.binary_op(left, right, op, line)

    if negate:
        target = builder.unary_op(target, "not", line)
    return target

