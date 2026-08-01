
def flatten_types_if_tuple(t: Type) -> list[Type]:
    """Flatten a nested sequence of tuples into one list of nodes."""
    t = get_proper_type(t)
    if isinstance(t, UnionType):
        return [UnionType.make_union([b for a in t.items for b in flatten_types_if_tuple(a)])]
    if isinstance(t, TupleType):
        return [b for a in t.items for b in flatten_types_if_tuple(a)]
    elif is_named_instance(t, "builtins.tuple"):
        return [t.args[0]]
    return [t]

