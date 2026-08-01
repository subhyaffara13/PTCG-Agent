
def ddm_irmul(a: list[list[R]], b: R) -> None:
    """a <-- b*a"""
    for ai in a:
        for j, aij in enumerate(ai):
            ai[j] = b * aij

