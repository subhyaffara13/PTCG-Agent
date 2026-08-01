
def _both_sets_are_equal(
    left: AbstractSet[object],
    right: AbstractSet[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
) -> Iterator[str]:
    yield "Both sets are equal"

