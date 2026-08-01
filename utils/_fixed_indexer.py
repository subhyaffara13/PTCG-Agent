
def _fixed_indexer(
    size: Sequence[int],
    stride: Sequence[int] | None = None,
    offset: Expr = Integer(0),
) -> Callable[[Sequence[Expr]], Expr]:
    """A closure containing math to read a given element"""

    def indexer(index: Sequence[int]) -> int:
        assert stride is not None and len(index) == len(stride)
        assert len(index) == len(size)
        result = offset
        for idx, st, sz in zip(index, stride, size):
            if sz != 1:
                result = result + idx * st
        return result

    return indexer

