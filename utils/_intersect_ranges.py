
def _intersect_ranges(
    left: Sequence[_VersionRange],
    right: Sequence[_VersionRange],
) -> list[_VersionRange]:
    """Intersect two sorted, non-overlapping range lists (two-pointer merge)."""
    result: list[_VersionRange] = []
    left_index = right_index = 0
    while left_index < len(left) and right_index < len(right):
        left_lower, left_upper = left[left_index]
        right_lower, right_upper = right[right_index]

        lower = max(left_lower, right_lower)
        upper = min(left_upper, right_upper)

        if not _range_is_empty(lower, upper):
            result.append((lower, upper))

        # Advance whichever side has the smaller upper bound.
        if left_upper < right_upper:
            left_index += 1
        else:
            right_index += 1

    return result


def _intersect_ranges(
    left: Sequence[_VersionRange],
    right: Sequence[_VersionRange],
) -> list[_VersionRange]:
    """Intersect two sorted, non-overlapping range lists (two-pointer merge)."""
    result: list[_VersionRange] = []
    left_index = right_index = 0
    while left_index < len(left) and right_index < len(right):
        left_lower, left_upper = left[left_index]
        right_lower, right_upper = right[right_index]

        lower = max(left_lower, right_lower)
        upper = min(left_upper, right_upper)

        if not _range_is_empty(lower, upper):
            result.append((lower, upper))

        # Advance whichever side has the smaller upper bound.
        if left_upper < right_upper:
            left_index += 1
        else:
            right_index += 1

    return result

