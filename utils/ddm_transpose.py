
def ddm_transpose(matrix: Sequence[Sequence[T]]) -> list[list[T]]:
    """matrix transpose"""
    return list(map(list, zip(*matrix)))

