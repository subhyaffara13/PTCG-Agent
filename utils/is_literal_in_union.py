
def is_literal_in_union(x: ProperType, y: ProperType) -> bool:
    """Return True if x is a Literal and y is an Union that includes x"""
    return (
        isinstance(x, LiteralType)
        and isinstance(y, UnionType)
        and any(x == get_proper_type(z) for z in y.items)
    )

