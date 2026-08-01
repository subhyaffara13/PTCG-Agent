
def matrix_to_zero(e):
    """Convert a zero matrix to the scalar zero."""
    if isinstance(e, MatrixBase):
        if zeros(*e.shape) == e:
            e = S.Zero
    elif isinstance(e, numpy_ndarray):
        e = _numpy_matrix_to_zero(e)
    elif isinstance(e, scipy_sparse_matrix):
        e = _scipy_sparse_matrix_to_zero(e)
    return e

