
def _det_laplace(M):
    """Compute the determinant of a matrix using Laplace expansion.

    While Laplace expansion is not the most efficient method of computing
    a determinant, it is a simple one, and it has the advantage of
    being division free. To improve efficiency, this function uses
    caching to avoid recomputing determinants of submatrices.
    """
    if not M.is_square:
        raise NonSquareMatrixError()
    if M.shape[0] == 0:
        return M.one
        # sympy/matrices/tests/test_matrices.py contains a test that
        # suggests that the determinant of a 0 x 0 matrix is one, by
        # convention.
    return __det_laplace(M.as_immutable())

