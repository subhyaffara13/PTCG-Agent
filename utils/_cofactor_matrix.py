
def _cofactor_matrix(M, method="berkowitz"):
    """Return a matrix containing the cofactor of each element.

    Parameters
    ==========

    method : string, optional
        Method to use to find the cofactors, can be "bareiss", "berkowitz",
        "bird", "laplace" or "lu".

    Examples
    ========

    >>> from sympy import Matrix
    >>> M = Matrix([[1, 2], [3, 4]])
    >>> M.cofactor_matrix()
    Matrix([
    [ 4, -3],
    [-2,  1]])

    See Also
    ========

    cofactor
    minor
    minor_submatrix
    """

    if not M.is_square:
        raise NonSquareMatrixError()

    return M._new(M.rows, M.cols,
            lambda i, j: M.cofactor(i, j, method))

