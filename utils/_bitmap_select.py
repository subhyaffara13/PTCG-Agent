
def _bitmap_select(s: int, seq: List[FrozenSet[int]]) -> Generator[FrozenSet[int], None, None]:
    """Select elements of ``seq`` which are marked by the bitmap set ``s``.

    E.g.:

        >>> list(_bitmap_select(0b11010, ['A', 'B', 'C', 'D', 'E']))
        ['B', 'D', 'E']
    """
    return (x for x, b in zip(seq, bin(s)[:1:-1]) if b == "1")

