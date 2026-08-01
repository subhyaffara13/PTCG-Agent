
def are_typed_dicts_overlapping(
    left: TypedDictType, right: TypedDictType, is_overlapping: Callable[[Type, Type], bool]
) -> bool:
    """Returns 'true' if left and right are overlapping TypeDictTypes."""
    # All required keys in left are present and overlapping with something in right
    for key in left.required_keys:
        if key not in right.items:
            return False
        if not is_overlapping(left.items[key], right.items[key]):
            return False

    # Repeat check in the other direction
    for key in right.required_keys:
        if key not in left.items:
            return False
        if not is_overlapping(left.items[key], right.items[key]):
            return False

    # The presence of any additional optional keys does not affect whether the two
    # TypedDicts are partially overlapping: the dicts would be overlapping if the
    # keys happened to be missing.
    return True

