
def sym_or(x: BoolLikeType, *others: BoolLikeType) -> BoolLikeType:
    """
    or, but for symbolic expressions, without bool casting.
    """
    if len(others) == 0:
        return x
    for y in others:
        x = operator.or_(x, y)
    return x

