
def isshape(x, nonneg=False, *, allow_nd=(2,), check_nd=True) -> bool:
    """Is x a valid tuple of dimensions?

    If nonneg, also checks that the dimensions are non-negative.
    Shapes of length in the tuple allow_nd are allowed.
    """
    ndim = len(x)
    if check_nd and ndim not in allow_nd:
        return False

    for d in x:
        if not isintlike(d):
            return False
        if nonneg and d < 0:
            return False
    return True

