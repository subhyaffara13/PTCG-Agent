
def _join_sorted_key(t: Type) -> int:
    t = get_proper_type(t)
    if isinstance(t, UnionType):
        return -2
    if isinstance(t, NoneType):
        return -1

    if isinstance(t, Overloaded):
        return 1
    return 0

