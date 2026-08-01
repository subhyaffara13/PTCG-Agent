
def ddm_iadd(a: list[list[R]], b: Sequence[Sequence[R]]) -> None:
    """a += b"""
    for ai, bi in zip(a, b):
        for j, bij in enumerate(bi):
            ai[j] += bij

