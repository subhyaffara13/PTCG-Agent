
def test_svds(X):
    u, s, vh = spla.svds(X, k=3)
    u2, s2, vh2 = np.linalg.svd(X.todense())
    s = np.sort(s)
    s2 = np.sort(s2[:3])
    npt.assert_allclose(s, s2, atol=1e-3)


def test_svds(matrices):
    A_dense, A_sparse, v0 = matrices

    u0, s0, vt0 = splin.svds(A_dense, k=2, v0=v0)
    u, s, vt = splin.svds(A_sparse, k=2, v0=v0)

    assert_allclose(s, s0)
    assert_allclose(np.abs(u), np.abs(u0))
    assert_allclose(np.abs(vt), np.abs(vt0))

