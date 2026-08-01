
def _minor(M, i, j, method="berkowitz"):
    """Return the (i,j) minor of ``M``.  That is,
    return the determinant of the matrix obtained by deleting
    the `i`th row and `j`th column from ``M``.

    Parameters
    ==========

    i, j : int
        The row and column to exclude to obtain the submatrix.

    method : string, optional
        Method to use to find the determinant of the submatrix, can be
        "bareiss", "berkowitz", "bird", "laplace" or "lu".

    Examples
    ========

    >>> from sympy import Matrix
    >>> M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> M.minor(1, 1)
    -12

    See Also
    ========

    minor_submatrix
    cofactor
    det
    """

    if not M.is_square:
        raise NonSquareMatrixError()

    return M.minor_submatrix(i, j).det(method=method)

