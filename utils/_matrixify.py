
def _matrixify(mat):
    """If `mat` is a Matrix or is matrix-like,
    return a Matrix or MatrixWrapper object.  Otherwise
    `mat` is passed through without modification."""

    if getattr(mat, 'is_Matrix', False) or getattr(mat, 'is_MatrixLike', False):
        return mat

    if not(getattr(mat, 'is_Matrix', True) or getattr(mat, 'is_MatrixLike', True)):
        return mat

    shape = None

    if hasattr(mat, 'shape'): # numpy, scipy.sparse
        if len(mat.shape) == 2:
            shape = mat.shape
    elif hasattr(mat, 'rows') and hasattr(mat, 'cols'): # mpmath
        shape = (mat.rows, mat.cols)

    if shape:
        return _MatrixWrapper(mat, shape)

    return mat

