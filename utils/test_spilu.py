
def test_spilu():
    X = scipy.sparse.csc_array([
        [1, 0, 0, 0],
        [2, 1, 0, 0],
        [3, 2, 1, 0],
        [4, 3, 2, 1],
    ])
    LU = spla.spilu(X)
    npt.assert_allclose(
        LU.solve(np.array([1, 2, 3, 4])),
        np.asarray([1, 0, 0, 0], dtype=np.float64),
        rtol=1e-14, atol=3e-16
    )


def test_spilu(matrices):
    A_dense, A_sparse, b = matrices
    sparse_cls = type(A_sparse)

    lu = splin.spilu(A_sparse)

    assert isinstance(lu.L, sparse_cls)
    assert isinstance(lu.U, sparse_cls)

    z = lu.solve(A_sparse.todense())
    assert_allclose(z, np.eye(len(b)), atol=1e-3)

