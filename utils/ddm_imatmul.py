
def ddm_imatmul(
    a: list[list[R]], b: Sequence[Sequence[R]], c: Sequence[Sequence[R]]
) -> None:
    """a += b @ c"""
    cT = list(zip(*c))

    for bi, ai in zip(b, a):
        for j, cTj in enumerate(cT):
            ai[j] = sum(map(mul, bi, cTj), ai[j])

