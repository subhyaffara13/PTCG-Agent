
def is_enum_overlapping_union(x: ProperType, y: ProperType) -> bool:
    """Return True if x is an Enum, and y is an Union with at least one Literal from x"""
    return (
        isinstance(x, Instance)
        and x.type.is_enum
        and isinstance(y, UnionType)
        and any(
            isinstance(p := get_proper_type(z), LiteralType) and x.type == p.fallback.type
            for z in y.relevant_items()
        )
    )

