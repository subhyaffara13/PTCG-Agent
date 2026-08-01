
def _compare_lt_set(
    left: AbstractSet[object],
    right: AbstractSet[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
) -> Iterator[str]:
    if left == right:
        yield "Both sets are equal"
    else:
        yield from _set_one_sided_diff("left", left, right, highlighter)

