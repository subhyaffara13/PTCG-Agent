
def _convert_matrix(typ, mat):
    """Convert mat to a Matrix of type typ."""
    from sympy.matrices.matrixbase import MatrixBase
    if getattr(mat, "is_Matrix", False) and not isinstance(mat, MatrixBase):
        # This is needed for interop between Matrix and the redundant matrix
        # mixin types like _MinimalMatrix etc. If anyone should happen to be
        # using those then this keeps them working. Really _MinimalMatrix etc
        # should be deprecated and removed though.
        return typ(*mat.shape, list(mat))
    else:
        return typ(mat)

