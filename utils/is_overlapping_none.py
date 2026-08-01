
def is_overlapping_none(t: Type) -> bool:
    t = get_proper_type(t)
    return isinstance(t, NoneType) or (
        isinstance(t, UnionType) and any(isinstance(get_proper_type(e), NoneType) for e in t.items)
    )

