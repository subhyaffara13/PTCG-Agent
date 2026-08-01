
def test_thin_hilbert(irl_mode, dtype):
    rng = np.random.default_rng(1757951587606893)
    m, n = 200, 4

    # Generate a Hilbert matrix of size m x n
    A = np.array([[1 / (i + j + 1) for j in range(n)] for i in range(m)], dtype=dtype)
    uu, ss, vv = np.linalg.svd(A, full_matrices=False)
    u, s, vt, _ = _svdp(A, k=4, which='LM', irl_mode=irl_mode, rng=rng)
    assert_allclose(s, ss, atol=TOLS[dtype])

    # Check orthogonality of singular vectors
    assert_allclose(np.eye(u.shape[1]), u.T @ u, atol=TOLS[dtype])
    assert_allclose(np.eye(vt.shape[0]), vt @ vt.T, atol=TOLS[dtype])

    # Check orthogonality against numpy svd results
    assert_allclose(np.abs(uu.T @ u), np.eye(n), atol=TOLS[dtype])
    assert_allclose(np.abs(vv @ vt.T), np.eye(n), atol=TOLS[dtype])

