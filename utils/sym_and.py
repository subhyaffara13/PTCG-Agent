
def sym_and(x: BoolLikeType, *others: BoolLikeType) -> BoolLikeType:
    """
    and, but for symbolic expressions, without bool casting.
    """
    if len(others) == 0:
        return x
    for y in others:
        x = operator.and_(x, y)
    return x

