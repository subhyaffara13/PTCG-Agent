
def has_none(a: tuple | int | None) -> bool:
    if is_tuple(a):
        return any(has_none(v) for v in a)
    else:
        return a is None

