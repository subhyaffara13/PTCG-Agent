
def _compare_eq_sequence(
    left: Sequence[object],
    right: Sequence[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
) -> Iterator[str]:
    comparing_bytes = isinstance(left, bytes) and isinstance(right, bytes)
    len_left = len(left)
    len_right = len(right)
    for i in range(min(len_left, len_right)):
        if left[i] != right[i]:
            if comparing_bytes:
                # when comparing bytes, we want to see their ascii representation
                # instead of their numeric values (#5260)
                # using a slice gives us the ascii representation:
                # >>> s = b'foo'
                # >>> s[0]
                # 102
                # >>> s[0:1]
                # b'f'
                left_value: object = left[i : i + 1]
                right_value: object = right[i : i + 1]
            else:
                left_value = left[i]
                right_value = right[i]

            yield (
                f"At index {i} diff:"
                f" {highlighter(repr(left_value))} != {highlighter(repr(right_value))}"
            )
            break

    if comparing_bytes:
        # when comparing bytes, it doesn't help to show the "sides contain one or more
        # items" longer explanation, so skip it
        return

    len_diff = len_left - len_right
    if len_diff:
        if len_diff > 0:
            dir_with_more = "Left"
            extra = saferepr(left[len_right])
        else:
            len_diff = 0 - len_diff
            dir_with_more = "Right"
            extra = saferepr(right[len_left])

        if len_diff == 1:
            yield f"{dir_with_more} contains one more item: {highlighter(extra)}"
        else:
            yield f"{dir_with_more} contains {len_diff} more items, first extra item: {highlighter(extra)}"

