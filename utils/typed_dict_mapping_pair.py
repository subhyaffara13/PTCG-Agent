
def typed_dict_mapping_pair(left: Type, right: Type) -> bool:
    """Is this a pair where one type is a TypedDict and another one is an instance of Mapping?

    This case requires a precise/principled consideration because there are two use cases
    that push the boundary the opposite ways: we need to avoid spurious overlaps to avoid
    false positives for overloads, but we also need to avoid spuriously non-overlapping types
    to avoid false positives with --strict-equality.
    """
    left, right = get_proper_types((left, right))
    assert not isinstance(left, TypedDictType) or not isinstance(right, TypedDictType)

    if isinstance(left, TypedDictType):
        _, other = left, right
    elif isinstance(right, TypedDictType):
        _, other = right, left
    else:
        return False
    return isinstance(other, Instance) and other.type.has_base("typing.Mapping")

