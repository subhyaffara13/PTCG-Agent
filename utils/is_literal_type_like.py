
def is_literal_type_like(t: Type | None) -> bool:
    """Returns 'true' if the given type context is potentially either a LiteralType,
    a Union of LiteralType, or something similar.
    """
    t = get_proper_type(t)
    if t is None:
        return False
    elif isinstance(t, LiteralType):
        return True
    elif isinstance(t, UnionType):
        return any(is_literal_type_like(item) for item in t.items)
    elif isinstance(t, TypeVarType):
        return is_literal_type_like(t.upper_bound) or any(
            is_literal_type_like(item) for item in t.values
        )
    else:
        return False

