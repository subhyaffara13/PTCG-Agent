
def _compare_gt_set(
    left: AbstractSet[object],
    right: AbstractSet[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
) -> Iterator[str]:
    if left == right:
        yield "Both sets are equal"
    else:
        yield from _set_one_sided_diff("right", right, left, highlighter)

