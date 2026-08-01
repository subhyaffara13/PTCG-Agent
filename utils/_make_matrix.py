
def _make_matrix(x):
    from sympy.matrices.immutable import ImmutableDenseMatrix
    if isinstance(x, MatrixExpr):
        return x
    return ImmutableDenseMatrix([[x]])

