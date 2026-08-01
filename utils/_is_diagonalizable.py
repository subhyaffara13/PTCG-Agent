
def _is_diagonalizable(M, reals_only=False, **kwargs):
    """Returns ``True`` if a matrix is diagonalizable.

    Parameters
    ==========

    reals_only : bool, optional
        If ``True``, it tests whether the matrix can be diagonalized
        to contain only real numbers on the diagonal.


        If ``False``, it tests whether the matrix can be diagonalized
        at all, even with numbers that may not be real.

    Examples
    ========

    Example of a diagonalizable matrix:

    >>> from sympy import Matrix
    >>> M = Matrix([[1, 2, 0], [0, 3, 0], [2, -4, 2]])
    >>> M.is_diagonalizable()
    True

    Example of a non-diagonalizable matrix:

    >>> M = Matrix([[0, 1], [0, 0]])
    >>> M.is_diagonalizable()
    False

    Example of a matrix that is diagonalized in terms of non-real entries:

    >>> M = Matrix([[0, 1], [-1, 0]])
    >>> M.is_diagonalizable(reals_only=False)
    True
    >>> M.is_diagonalizable(reals_only=True)
    False

    See Also
    ========

    sympy.matrices.matrixbase.MatrixBase.is_diagonal
    diagonalize
    """
    if not M.is_square:
        return False

    if all(e.is_real for e in M) and M.is_symmetric():
        return True

    if all(e.is_complex for e in M) and M.is_hermitian:
        return True

    return _is_diagonalizable_with_eigen(M, reals_only=reals_only)[0]

