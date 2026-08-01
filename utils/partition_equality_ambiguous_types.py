
def partition_equality_ambiguous_types(
    current_type: Type, target_type: Type, *, is_identity: bool
) -> tuple[Type | None, Type | None]:
    """Split current_type into ordinary-narrowable and equality-ambiguous pieces.

    Some values compare equal through a value domain broader than their nominal type. For
    example, an IntEnum member can compare equal to an int, and a StrEnum member can compare
    equal to a str. When narrowing `x: MyStrEnum | str` against `MyStrEnum.MEMBER`, we can
    still narrow the enum portion of the union, but we must keep the str portion in both
    branches.
    """
    if is_identity:
        return current_type, None

    typ = get_proper_type(current_type)
    items = typ.relevant_items() if isinstance(typ, UnionType) else [current_type]
    narrowable_items = []
    ambiguous_items = []
    for item in items:
        if is_equality_ambiguous_for_narrowing(item, target_type):
            ambiguous_items.append(item)
        else:
            narrowable_items.append(item)
    return (
        UnionType.make_union(narrowable_items) if narrowable_items else None,
        UnionType.make_union(ambiguous_items) if ambiguous_items else None,
    )

