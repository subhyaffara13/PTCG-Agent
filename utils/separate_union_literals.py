
def separate_union_literals(t: UnionType) -> tuple[Sequence[LiteralType], Sequence[Type]]:
    """Separate literals from other members in a union type."""
    literal_items = []
    union_items = []

    for item in t.items:
        proper = get_proper_type(item)
        if isinstance(proper, LiteralType):
            literal_items.append(proper)
        else:
            union_items.append(item)

    return literal_items, union_items

