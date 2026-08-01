
def _normalize_extras(
    result: MarkerList | MarkerAtom | str,
) -> MarkerList | MarkerAtom | str:
    if not isinstance(result, tuple):
        return result

    lhs, op, rhs = result
    if isinstance(lhs, Variable) and lhs.value == "extra":
        normalized_extra = canonicalize_name(rhs.value)
        rhs = Value(normalized_extra)
    elif isinstance(rhs, Variable) and rhs.value == "extra":
        normalized_extra = canonicalize_name(lhs.value)
        lhs = Value(normalized_extra)
    return lhs, op, rhs


def _normalize_extras(
    result: MarkerList | MarkerAtom | str,
) -> MarkerList | MarkerAtom | str:
    if not isinstance(result, tuple):
        return result

    lhs, op, rhs = result
    if isinstance(lhs, Variable) and lhs.value == "extra":
        normalized_extra = canonicalize_name(rhs.value)
        rhs = Value(normalized_extra)
    elif isinstance(rhs, Variable) and rhs.value == "extra":
        normalized_extra = canonicalize_name(lhs.value)
        lhs = Value(normalized_extra)
    return lhs, op, rhs


def _normalize_extras(
    result: MarkerList | MarkerAtom | str,
) -> MarkerList | MarkerAtom | str:
    if not isinstance(result, tuple):
        return result

    lhs, op, rhs = result
    if isinstance(lhs, Variable) and lhs.value == "extra":
        normalized_extra = canonicalize_name(rhs.value)
        rhs = Value(normalized_extra)
    elif isinstance(rhs, Variable) and rhs.value == "extra":
        normalized_extra = canonicalize_name(lhs.value)
        lhs = Value(normalized_extra)
    return lhs, op, rhs

