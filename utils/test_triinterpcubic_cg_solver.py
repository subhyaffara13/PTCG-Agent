
def test_triinterpcubic_cg_solver():
    # Now 3 basic tests of the Sparse CG solver, used for
    # TriCubicInterpolator with *kind* = 'min_E'
    # 1) A commonly used test involves a 2d Poisson matrix.
    def poisson_sparse_matrix(n, m):
        """
        Return the sparse, (n*m, n*m) matrix in COO format resulting from the
        discretisation of the 2-dimensional Poisson equation according to a
        finite difference numerical scheme on a uniform (n, m) grid.
        """
        l = m*n
        rows = np.concatenate([
            np.arange(l, dtype=np.int32),
            np.arange(l-1, dtype=np.int32), np.arange(1, l, dtype=np.int32),
            np.arange(l-n, dtype=np.int32), np.arange(n, l, dtype=np.int32)])
        cols = np.concatenate([
            np.arange(l, dtype=np.int32),
            np.arange(1, l, dtype=np.int32), np.arange(l-1, dtype=np.int32),
            np.arange(n, l, dtype=np.int32), np.arange(l-n, dtype=np.int32)])
        vals = np.concatenate([
            4*np.ones(l, dtype=np.float64),
            -np.ones(l-1, dtype=np.float64), -np.ones(l-1, dtype=np.float64),
            -np.ones(l-n, dtype=np.float64), -np.ones(l-n, dtype=np.float64)])
        # In fact +1 and -1 diags have some zeros
        vals[l:2*l-1][m-1::m] = 0.
        vals[2*l-1:3*l-2][m-1::m] = 0.
        return vals, rows, cols, (n*m, n*m)

    # Instantiating a sparse Poisson matrix of size 48 x 48:
    (n, m) = (12, 4)
    mat = mtri._triinterpolate._Sparse_Matrix_coo(*poisson_sparse_matrix(n, m))
    mat.compress_csc()
    mat_dense = mat.to_dense()
    # Testing a sparse solve for all 48 basis vector
    for itest in range(n*m):
        b = np.zeros(n*m, dtype=np.float64)
        b[itest] = 1.
        x, _ = mtri._triinterpolate._cg(A=mat, b=b, x0=np.zeros(n*m),
                                        tol=1.e-10)
        assert_array_almost_equal(np.dot(mat_dense, x), b)

    # 2) Same matrix with inserting 2 rows - cols with null diag terms
    # (but still linked with the rest of the matrix by extra-diag terms)
    (i_zero, j_zero) = (12, 49)
    vals, rows, cols, _ = poisson_sparse_matrix(n, m)
    rows = rows + 1*(rows >= i_zero) + 1*(rows >= j_zero)
    cols = cols + 1*(cols >= i_zero) + 1*(cols >= j_zero)
    # adding extra-diag terms
    rows = np.concatenate([rows, [i_zero, i_zero-1, j_zero, j_zero-1]])
    cols = np.concatenate([cols, [i_zero-1, i_zero, j_zero-1, j_zero]])
    vals = np.concatenate([vals, [1., 1., 1., 1.]])
    mat = mtri._triinterpolate._Sparse_Matrix_coo(vals, rows, cols,
                                                  (n*m + 2, n*m + 2))
    mat.compress_csc()
    mat_dense = mat.to_dense()
    # Testing a sparse solve for all 50 basis vec
    for itest in range(n*m + 2):
        b = np.zeros(n*m + 2, dtype=np.float64)
        b[itest] = 1.
        x, _ = mtri._triinterpolate._cg(A=mat, b=b, x0=np.ones(n * m + 2),
                                        tol=1.e-10)
        assert_array_almost_equal(np.dot(mat_dense, x), b)

    # 3) Now a simple test that summation of duplicate (i.e. with same rows,
    # same cols) entries occurs when compressed.
    vals = np.ones(17, dtype=np.float64)
    rows = np.array([0, 1, 2, 0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1],
                    dtype=np.int32)
    cols = np.array([0, 1, 2, 1, 1, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                    dtype=np.int32)
    dim = (3, 3)
    mat = mtri._triinterpolate._Sparse_Matrix_coo(vals, rows, cols, dim)
    mat.compress_csc()
    mat_dense = mat.to_dense()
    assert_array_almost_equal(mat_dense, np.array([
        [1., 2., 0.], [2., 1., 5.], [0., 5., 1.]], dtype=np.float64))

