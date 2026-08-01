
def _det_berkowitz(M):
    """ Use the Berkowitz algorithm to compute the determinant."""

    if not M.is_square:
        raise NonSquareMatrixError()

    if M.rows == 0:
        return M.one
        # sympy/matrices/tests/test_matrices.py contains a test that
        # suggests that the determinant of a 0 x 0 matrix is one, by
        # convention.

    berk_vector = _berkowitz_vector(M)
    return (-1)**(len(berk_vector) - 1) * berk_vector[-1]

