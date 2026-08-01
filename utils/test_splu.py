
def test_splu():
    X = scipy.sparse.csc_array([
        [1, 0, 0, 0],
        [2, 1, 0, 0],
        [3, 2, 1, 0],
        [4, 3, 2, 1],
    ])
    LU = spla.splu(X)
    npt.assert_allclose(
        LU.solve(np.array([1, 2, 3, 4])),
        np.asarray([1, 0, 0, 0], dtype=np.float64),
        rtol=1e-14, atol=3e-16
    )


def test_splu(matrices):
    A_dense, A_sparse, b = matrices
    n = len(b)
    sparse_cls = type(A_sparse)

    lu = splin.splu(A_sparse)

    assert isinstance(lu.L, sparse_cls)
    assert isinstance(lu.U, sparse_cls)

    _Pr_scipy = sp.csc_array((np.ones(n), (lu.perm_r, np.arange(n))))
    _Pc_scipy = sp.csc_array((np.ones(n), (np.arange(n), lu.perm_c)))
    Pr = sparse_cls.from_scipy_sparse(_Pr_scipy)
    Pc = sparse_cls.from_scipy_sparse(_Pc_scipy)
    A2 = Pr.T @ lu.L @ lu.U @ Pc.T

    assert_allclose(A2.todense(), A_sparse.todense())

    z = lu.solve(A_sparse.todense())
    assert_allclose(z, np.eye(n), atol=1e-10)

