
def test_fat_random(dtype):
    rng = np.random.default_rng(1758046113948869)
    m, n = 3, 100

    A = rng.uniform(size=(m, n)).astype(dtype)
    if dtype in (np.complex64, np.complex128):
        A += dtype(1j) * rng.uniform(size=(m, n)).astype(dtype)

    uu, ss, vv = np.linalg.svd(A, full_matrices=False)
    u, s, vt, _ = _svdp(A, k=3, which='LM', irl_mode=True, rng=rng)
    assert_allclose(s, ss, atol=TOLS[dtype])

    # Check orthogonality of singular vectors
    assert_allclose(np.eye(u.shape[1]), u.conj().T @ u, atol=TOLS[dtype])
    assert_allclose(np.eye(vt.shape[0]), vt @ vt.conj().T, atol=TOLS[dtype])

    # Check orthogonality against numpy svd results
    assert_allclose(np.abs(uu.conj().T @ u), np.eye(m), atol=TOLS[dtype])
    assert_allclose(np.abs(vv @ vt.conj().T), np.eye(m), atol=TOLS[dtype])

