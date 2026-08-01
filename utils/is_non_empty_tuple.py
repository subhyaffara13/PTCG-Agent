
def is_non_empty_tuple(t: Type) -> bool:
    t = get_proper_type(t)
    return isinstance(t, TupleType) and bool(t.items)

