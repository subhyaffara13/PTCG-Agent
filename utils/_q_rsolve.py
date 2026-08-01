
def _QRsolve(M, b):
    """Solve the linear system ``Ax = b``.

    ``M`` is the matrix ``A``, the method argument is the vector
    ``b``.  The method returns the solution vector ``x``.  If ``b`` is a
    matrix, the system is solved for each column of ``b`` and the
    return value is a matrix of the same shape as ``b``.

    This method is slower (approximately by a factor of 2) but
    more stable for floating-point arithmetic than the LUsolve method.
    However, LUsolve usually uses an exact arithmetic, so you do not need
    to use QRsolve.

    This is mainly for educational purposes and symbolic matrices, for real
    (or complex) matrices use mpmath.qr_solve.

    See Also
    ========

    sympy.matrices.dense.DenseMatrix.lower_triangular_solve
    sympy.matrices.dense.DenseMatrix.upper_triangular_solve
    gauss_jordan_solve
    cholesky_solve
    diagonal_solve
    LDLsolve
    LUsolve
    pinv_solve
    QRdecomposition
    cramer_solve
    """

    dps  = _get_intermediate_simp(expand_mul, expand_mul)
    Q, R = M.QRdecomposition()
    y    = Q.T * b

    # back substitution to solve R*x = y:
    # We build up the result "backwards" in the vector 'x' and reverse it
    # only in the end.
    x = []
    n = R.rows

    for j in range(n - 1, -1, -1):
        tmp = y[j, :]

        for k in range(j + 1, n):
            tmp -= R[j, k] * x[n - 1 - k]

        tmp = dps(tmp)

        x.append(tmp / R[j, j])

    return M.vstack(*x[::-1])

