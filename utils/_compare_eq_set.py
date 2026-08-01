
def _compare_eq_set(
    left: AbstractSet[object],
    right: AbstractSet[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
) -> Iterator[str]:
    yield from _set_one_sided_diff("left", left, right, highlighter)
    yield from _set_one_sided_diff("right", right, left, highlighter)

