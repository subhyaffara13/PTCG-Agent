from typing import Callable

def are_tuples_overlapping(
    left: Type, right: Type, is_overlapping: Callable[[Type, Type], bool]
) -> bool:
    """Returns true if left and right are overlapping tuples."""
    left, right = get_proper_types((left, right))
    left = adjust_tuple(left, right) or left
    right = adjust_tuple(right, left) or right
    assert isinstance(left, TupleType), f"Type {left} is not a tuple"
    assert isinstance(right, TupleType), f"Type {right} is not a tuple"

    # This algorithm works well if only one tuple is variadic, if both are
    # variadic we may get rare false negatives for overlapping prefix/suffix.
    # Also, this ignores empty unpack case, but it is probably consistent with
    # how we handle e.g. empty lists in overload overlaps.
    # TODO: write a more robust algorithm for cases where both types are variadic.
    left_unpack = find_unpack_in_list(left.items)
    right_unpack = find_unpack_in_list(right.items)
    if left_unpack is not None:
        left = expand_tuple_if_possible(left, len(right.items))
    if right_unpack is not None:
        right = expand_tuple_if_possible(right, len(left.items))

    if len(left.items) != len(right.items):
        return False
    if not all(is_overlapping(l, r) for l, r in zip(left.items, right.items)):
        return False

    # Check that the tuples aren't from e.g. different NamedTuples.
    if is_named_instance(right.partial_fallback, "builtins.tuple") or is_named_instance(
        left.partial_fallback, "builtins.tuple"
    ):
        return True
    else:
        return is_overlapping(left.partial_fallback, right.partial_fallback)

