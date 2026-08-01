
def constant_fold_binary_int_op(op: str, left: int, right: int) -> int | float | None:
    if op == "+":
        return left + right
    if op == "-":
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
    elif op == "&":
        return left & right
    elif op == "|":
        return left | right
    elif op == "^":
        return left ^ right
    elif op == "<<":
        if right >= 0:
            return left << right
    elif op == ">>":
        if right >= 0:
            return left >> right
    elif op == "**":
        if right >= 0:
            ret = left**right
            assert isinstance(ret, int)
            return ret
    return None

