
def constant_fold_binary_op(
    op: str, left: ConstantValue, right: ConstantValue
) -> ConstantValue | None:
    if isinstance(left, int) and isinstance(right, int):
        return constant_fold_binary_int_op(op, left, right)

    # Float and mixed int/float arithmetic.
    if isinstance(left, float) and isinstance(right, float):
        return constant_fold_binary_float_op(op, left, right)
    elif isinstance(left, float) and isinstance(right, int):
        return constant_fold_binary_float_op(op, left, right)
    elif isinstance(left, int) and isinstance(right, float):
        return constant_fold_binary_float_op(op, left, right)

    # String concatenation and multiplication.
    if op == "+" and isinstance(left, str) and isinstance(right, str):
        return left + right
    elif op == "*" and isinstance(left, str) and isinstance(right, int):
        return left * right
    elif op == "*" and isinstance(left, int) and isinstance(right, str):
        return left * right

    # Complex construction.
    if op == "+" and isinstance(left, (int, float)) and isinstance(right, complex):
        return left + right
    elif op == "+" and isinstance(left, complex) and isinstance(right, (int, float)):
        return left + right
    elif op == "-" and isinstance(left, (int, float)) and isinstance(right, complex):
        return left - right
    elif op == "-" and isinstance(left, complex) and isinstance(right, (int, float)):
        return left - right

    return None

