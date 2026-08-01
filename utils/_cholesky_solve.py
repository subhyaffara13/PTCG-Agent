
def _cholesky_solve(M, rhs):
    """Solves ``Ax = B`` using Cholesky decomposition,
    for a general square non-singular matrix.
    For a non-square matrix with rows > cols,
    the least squares solution is returned.

    See Also
    ========

    sympy.matrices.dense.DenseMatrix.lower_triangular_solve
    sympy.matrices.dense.DenseMatrix.upper_triangular_solve
    gauss_jordan_solve
    diagonal_solve
    LDLsolve
    LUsolve
    QRsolve
    pinv_solve
    cramer_solve
    """

    if M.rows < M.cols:
        raise NotImplementedError(
            'Under-determined System. Try M.gauss_jordan_solve(rhs)')

    hermitian = True
    reform    = False

    if M.is_symmetric():
        hermitian = False
    elif not M.is_hermitian:
        reform = True

    if reform or _fuzzy_positive_definite(M) is False:
        H         = M.H
        M         = H.multiply(M)
        rhs       = H.multiply(rhs)
        hermitian = not M.is_symmetric()

    L = M.cholesky(hermitian=hermitian)
    Y = L.lower_triangular_solve(rhs)

    if hermitian:
        return (L.H).upper_triangular_solve(Y)
    else:
        return (L.T).upper_triangular_solve(Y)

