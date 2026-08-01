
def check_svdp(n, m, constructor, dtype, k, irl_mode, which, f=0.8, rng=None):
    tol = TOLS[dtype]

    if rng is None:
        rng = np.random.default_rng(0)

    # Legacy clamp for the generator
    rng2 = np.random.default_rng(0)
    if is_complex_type(dtype):
        M = (- 5 + 10 * rng2.uniform(size=[n, m])
             - 5j + 10j * rng2.uniform(size=[n, m])).astype(dtype)
    else:
        M = (-5 + 10 * rng2.uniform(size=[n, m])).astype(dtype)
    M[M.real > 10 * f - 5] = 0
    Msp = constructor(M)

    u1, sigma1, vt1 = np.linalg.svd(M, full_matrices=False)
    u2, sigma2, vt2, _ = _svdp(Msp, k=k,which=which, irl_mode=irl_mode,
                               tol=tol, rng=rng)

    # check the which
    if which.upper() == 'SM':
        u1 = np.roll(u1, k, 1)
        vt1 = np.roll(vt1, k, 0)
        sigma1 = np.roll(sigma1, k)

    # check that singular values agree
    assert_allclose(sigma1[:k], sigma2, rtol=tol, atol=tol)

    # check that singular vectors are orthogonal
    assert_allclose(np.abs(u1.conj().T @ u2), np.eye(n, k), rtol=tol, atol=tol)
    assert_allclose(np.abs(vt1.conj() @ vt2.T), np.eye(n, k), rtol=tol, atol=tol)

