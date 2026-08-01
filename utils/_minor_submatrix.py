
def _minor_submatrix(M, i, j):
    """Return the submatrix obtained by removing the `i`th row
    and `j`th column from ``M`` (works with Pythonic negative indices).

    Parameters
    ==========

    i, j : int
        The row and column to exclude to obtain the submatrix.

    Examples
    ========

    >>> from sympy import Matrix
    >>> M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> M.minor_submatrix(1, 1)
    Matrix([
    [1, 3],
    [7, 9]])

    See Also
    ========

    minor
    cofactor
    """

    if i < 0:
        i += M.rows
    if j < 0:
        j += M.cols

    if not 0 <= i < M.rows or not 0 <= j < M.cols:
        raise ValueError("`i` and `j` must satisfy 0 <= i < ``M.rows`` "
                            "(%d)" % M.rows + "and 0 <= j < ``M.cols`` (%d)." % M.cols)

    rows = [a for a in range(M.rows) if a != i]
    cols = [a for a in range(M.cols) if a != j]

    return M.extract(rows, cols)

