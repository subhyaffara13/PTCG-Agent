
def _arrayfy(a):
    from sympy.matrices import MatrixBase

    if isinstance(a, NDimArray):
        return a
    if isinstance(a, (MatrixBase, list, tuple, Tuple)):
        return ImmutableDenseNDimArray(a)
    return a

