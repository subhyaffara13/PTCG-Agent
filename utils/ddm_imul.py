
def ddm_imul(a: list[list[R]], b: R) -> None:
    """a <-- a*b"""
    for ai in a:
        for j, aij in enumerate(ai):
            ai[j] = aij * b

