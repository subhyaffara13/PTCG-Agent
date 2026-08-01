
def _check_svds_n(A, k, u, s, vh, which="LM", check_res=True,
                  check_svd=True, atol=1e-10, rtol=1e-7):
    n, m = A.shape

    # Check shapes.
    assert_equal(u.shape, (n, k))
    assert_equal(s.shape, (k,))
    assert_equal(vh.shape, (k, m))

    # Check that u is a semi-orthogonal matrix.
    uh_u = np.dot(u.T.conj(), u)
    assert_equal(uh_u.shape, (k, k))
    error = np.sum(np.abs(uh_u - np.identity(k))) / (k * k)
    assert_allclose(error, 0.0, atol=atol, rtol=rtol)

    # Check that vh is a semi-orthogonal matrix.
    vh_v = np.dot(vh, vh.T.conj())
    assert_equal(vh_v.shape, (k, k))
    error = np.sum(np.abs(vh_v - np.identity(k))) / (k * k)
    assert_allclose(error, 0.0, atol=atol, rtol=rtol)

    # Check residuals
    if check_res:
        ru = A.T.conj() @ u - vh.T.conj() * s
        rus = np.sum(np.abs(ru)) / (n * k)
        rvh = A @ vh.T.conj() - u * s
        rvhs = np.sum(np.abs(rvh)) / (m * k)
        assert_allclose(rus, 0.0, atol=atol, rtol=rtol)
        assert_allclose(rvhs, 0.0, atol=atol, rtol=rtol)

    # Check that scipy.sparse.linalg.svds ~ scipy.linalg.svd
    if check_svd:
        u2, s2, vh2 = sorted_svd(A, k, which)
        assert_allclose(s, s2, atol=atol, rtol=rtol)
        A_rebuilt_svd = (u2*s2).dot(vh2)
        A_rebuilt = (u*s).dot(vh)
        assert_equal(A_rebuilt.shape, A.shape)
        error = np.sum(np.abs(A_rebuilt_svd - A_rebuilt)) / (k * k)
        assert_allclose(error, 0.0, atol=atol, rtol=rtol)

