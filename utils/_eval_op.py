from typing import Optional

def _eval_op(lhs: str, op: Op, rhs: str | AbstractSet[str], *, key: str) -> bool:
    op_str = op.serialize()
    if key in MARKERS_REQUIRING_VERSION:
        try:
            spec = Specifier(f"{op_str}{rhs}")
        except InvalidSpecifier:
            pass
        else:
            return spec.contains(lhs, prereleases=True)

    oper: Operator | None = _operators.get(op_str)
    if oper is None:
        raise UndefinedComparison(f"Undefined {op!r} on {lhs!r} and {rhs!r}.")

    return oper(lhs, rhs)


def _eval_op(lhs: str, op: Op, rhs: str | AbstractSet[str], *, key: str) -> bool:
    op_str = op.serialize()
    if key in MARKERS_REQUIRING_VERSION:
        try:
            spec = Specifier(f"{op_str}{rhs}")
        except InvalidSpecifier:
            pass
        else:
            return spec.contains(lhs, prereleases=True)

    oper: Operator | None = _operators.get(op_str)
    if oper is None:
        raise UndefinedComparison(f"Undefined {op!r} on {lhs!r} and {rhs!r}.")

    return oper(lhs, rhs)


def _eval_op(lhs: str, op: Op, rhs: str) -> bool:
    try:
        spec = Specifier("".join([op.serialize(), rhs]))
    except InvalidSpecifier:
        pass
    else:
        return spec.contains(lhs)

    oper: Optional[Operator] = _operators.get(op.serialize())
    if oper is None:
        raise UndefinedComparison(f"Undefined {op!r} on {lhs!r} and {rhs!r}.")

    return oper(lhs, rhs)


def _eval_op(lhs: str, op: Op, rhs: str | AbstractSet[str], *, key: str) -> bool:
    op_str = op.serialize()
    if key in MARKERS_REQUIRING_VERSION:
        try:
            spec = Specifier(f"{op_str}{rhs}")
        except InvalidSpecifier:
            pass
        else:
            return spec.contains(lhs, prereleases=True)

    oper: Operator | None = _operators.get(op_str)
    if oper is None:
        raise UndefinedComparison(f"Undefined {op!r} on {lhs!r} and {rhs!r}.")

    return oper(lhs, rhs)

