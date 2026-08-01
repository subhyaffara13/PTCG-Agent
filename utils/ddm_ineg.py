
def ddm_ineg(a: list[list[R]]) -> None:
    """a <-- -a"""
    for ai in a:
        for j, aij in enumerate(ai):
            ai[j] = -aij

