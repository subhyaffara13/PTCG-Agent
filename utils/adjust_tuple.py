
def adjust_tuple(left: ProperType, r: ProperType) -> TupleType | None:
    """Find out if `left` is a Tuple[A, ...], and adjust its length to `right`"""
    if isinstance(left, Instance) and left.type.fullname == "builtins.tuple":
        n = r.length() if isinstance(r, TupleType) else 1
        return TupleType([left.args[0]] * n, left)
    return None

