
def constant_fold_binary_float_op(op: str, left: int | float, right: int | float) -> float | None:
    assert not (isinstance(left, int) and isinstance(right, int)), (op, left, right)
    if op == "+":
        return left + right
    elif op == "-":
        return left - right
    elif op == "*":
        return left * right
    elif op == "/":
        if right != 0:
            return left / right
    elif op == "//":
        if right != 0:
            return left // right
    elif op == "%":
        if right != 0:
            return left % right
    elif op == "**":
        if (left < 0 and isinstance(right, int)) or left > 0:
            try:
                ret = left**right
            except OverflowError:
                return None
            else:
                assert isinstance(ret, float), ret
                return ret

    return None

