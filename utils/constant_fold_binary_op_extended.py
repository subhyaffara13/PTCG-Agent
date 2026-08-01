
def constant_fold_binary_op_extended(
    op: str, left: ConstantValue, right: ConstantValue
) -> ConstantValue | None:
    """Like mypy's constant_fold_binary_op(), but includes bytes support.

    mypy cannot use constant folded bytes easily so it's simpler to only support them in mypyc.
    """
    if not isinstance(left, bytes) and not isinstance(right, bytes):
        return constant_fold_binary_op(op, left, right)

    if op == "+" and isinstance(left, bytes) and isinstance(right, bytes):
        return left + right
    elif op == "*" and isinstance(left, bytes) and isinstance(right, int):
        return left * right
    elif op == "*" and isinstance(left, int) and isinstance(right, bytes):
        return left * right

    return None

