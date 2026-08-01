
def list_cmp(
    op: Callable[[Any, Any], bool], left: Sequence[T], right: Sequence[T]
) -> bool:
    """emulate `(1,2,3) > (1,2)` etc"""

    # Optimization: For equality, short-circuit if lengths differ
    # This avoids iterating through elements and triggering guards on SymInts
    left_len = len(left)
    right_len = len(right)

    if op is eq and left_len != right_len:
        return False
    if op is ne and left_len != right_len:
        return True

    # Apply `op` to the first pair that differ
    for a, b in zip(left, right):
        if a != b:
            return op(a, b)

    # No more pairs to compare, so compare sizes.
    return op(left_len, right_len)

