
def test_spsolve_triangular(fmt):
    arr = [
        [1, 0, 0, 0],
        [2, 1, 0, 0],
        [3, 2, 1, 0],
        [4, 3, 2, 1],
    ]
    if fmt == "csr":
      X = scipy.sparse.csr_array(arr)
    else:
      X = scipy.sparse.csc_array(arr)
    spla.spsolve_triangular(X, [1, 2, 3, 4])


def test_spsolve_triangular(matrices):
    A_dense, A_sparse, b = matrices
    A_sparse = sparse.tril(A_sparse)

    x = splin.spsolve_triangular(A_sparse, b)
    assert_allclose(A_sparse @ x, b)

