
def test_spsolve(B):
    if B.__class__.__name__[:3] not in ('csc', 'csr'):
        return

    npt.assert_allclose(
        spla.spsolve(B, [1, 2]),
        np.linalg.solve(B.todense(), [1, 2])
    )


def test_spsolve(matrices):
    A_dense, A_sparse, b = matrices
    b2 = np.random.rand(len(b), 3)

    x0 = splin.spsolve(sp.csc_array(A_dense), b)
    x = splin.spsolve(A_sparse, b)
    assert isinstance(x, np.ndarray)
    assert_allclose(x, x0)

    x0 = splin.spsolve(sp.csc_array(A_dense), b)
    x = splin.spsolve(A_sparse, b, use_umfpack=True)
    assert isinstance(x, np.ndarray)
    assert_allclose(x, x0)

    x0 = splin.spsolve(sp.csc_array(A_dense), b2)
    x = splin.spsolve(A_sparse, b2)
    assert isinstance(x, np.ndarray)
    assert_allclose(x, x0)

    x0 = splin.spsolve(sp.csc_array(A_dense),
                       sp.csc_array(A_dense))
    x = splin.spsolve(A_sparse, A_sparse)
    assert isinstance(x, type(A_sparse))
    assert_allclose(x.todense(), x0.todense())

