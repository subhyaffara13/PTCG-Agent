
def _check_svds(A, k, u, s, vh, which="LM", check_usvh_A=False,
                check_svd=True, atol=1e-10, rtol=1e-7):
    n, m = A.shape

    # Check shapes.
    assert_equal(u.shape, (n, k))
    assert_equal(s.shape, (k,))
    assert_equal(vh.shape, (k, m))

    # Check that the original matrix can be reconstituted.
    A_rebuilt = (u*s).dot(vh)
    assert_equal(A_rebuilt.shape, A.shape)
    if check_usvh_A:
        assert_allclose(A_rebuilt, A, atol=atol, rtol=rtol)

    # Check that u is a semi-orthogonal matrix.
    uh_u = np.dot(u.T.conj(), u)
    assert_equal(uh_u.shape, (k, k))
    assert_allclose(uh_u, np.identity(k), atol=atol, rtol=rtol)

    # Check that vh is a semi-orthogonal matrix.
    vh_v = np.dot(vh, vh.T.conj())
    assert_equal(vh_v.shape, (k, k))
    assert_allclose(vh_v, np.identity(k), atol=atol, rtol=rtol)

    # Check that scipy.sparse.linalg.svds ~ scipy.linalg.svd
    if check_svd:
        u2, s2, vh2 = sorted_svd(A, k, which)
        assert_allclose(np.abs(u), np.abs(u2), atol=atol, rtol=rtol)
        assert_allclose(s, s2, atol=atol, rtol=rtol)
        assert_allclose(np.abs(vh), np.abs(vh2), atol=atol, rtol=rtol)

