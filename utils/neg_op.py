
def neg_op(op: int) -> int:
    """Map SubtypeOf to SupertypeOf and vice versa."""

    if op == SUBTYPE_OF:
        return SUPERTYPE_OF
    elif op == SUPERTYPE_OF:
        return SUBTYPE_OF
    else:
        raise ValueError(f"Invalid operator {op}")

