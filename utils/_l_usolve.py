
def _LUsolve(M, rhs, iszerofunc=_iszero):
    """Solve the linear system ``Ax = rhs`` for ``x`` where ``A = M``.

    This is for symbolic matrices, for real or complex ones use
    mpmath.lu_solve or mpmath.qr_solve.

    See Also
    ========

    sympy.matrices.dense.DenseMatrix.lower_triangular_solve
    sympy.matrices.dense.DenseMatrix.upper_triangular_solve
    gauss_jordan_solve
    cholesky_solve
    diagonal_solve
    LDLsolve
    QRsolve
    pinv_solve
    LUdecomposition
    cramer_solve
    """

    if rhs.rows != M.rows:
        raise ShapeError(
            "``M`` and ``rhs`` must have the same number of rows.")

    m = M.rows
    n = M.cols

    if m < n:
        raise NotImplementedError("Underdetermined systems not supported.")

    try:
        A, perm = M.LUdecomposition_Simple(
            iszerofunc=iszerofunc, rankcheck=True)
    except ValueError:
        raise NonInvertibleMatrixError("Matrix det == 0; not invertible.")

    dps = _get_intermediate_simp()
    b   = rhs.permute_rows(perm).as_mutable()

    # forward substitution, all diag entries are scaled to 1
    for i in range(m):
        for j in range(min(i, n)):
            scale = A[i, j]
            b.zip_row_op(i, j, lambda x, y: dps(x - scale * y))

    # consistency check for overdetermined systems
    if m > n:
        for i in range(n, m):
            for j in range(b.cols):
                if not iszerofunc(b[i, j]):
                    raise ValueError("The system is inconsistent.")

        b = b[0:n, :]   # truncate zero rows if consistent

    # backward substitution
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            scale = A[i, j]
            b.zip_row_op(i, j, lambda x, y: dps(x - scale * y))

        scale = A[i, i]
        b.row_op(i, lambda x, _: dps(scale**-1 * x))

    return rhs.__class__(b)

