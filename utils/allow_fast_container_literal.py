
def allow_fast_container_literal(t: Type) -> bool:
    if isinstance(t, TypeAliasType) and t.is_recursive:
        return False
    t = get_proper_type(t)
    return isinstance(t, Instance) or (
        isinstance(t, TupleType) and all(allow_fast_container_literal(it) for it in t.items)
    )

