
def test_funm_multiply_krylov_types(dtype_a, dtype_b):
    assert_allclose_ = (partial(assert_allclose, rtol = 1.8e-3, atol = 1e-5)
                        if {dtype_a, dtype_b} else assert_allclose)

    rng = np.random.default_rng(1738151906092735)
    n = 50

    if dtype_a in REAL_DTYPES:
        A = rng.random([n, n]).astype(dtype_a)
    else:
        A = (rng.random([n, n]) + 1j * rng.random([n, n])).astype(dtype_a)

    if dtype_b in REAL_DTYPES:
        b = (2 * rng.random(n)).astype(dtype_b)
    else:
        b = (rng.random(n) + 1j * rng.random(n)).astype(dtype_b)

        expA = expm(A)
        expected = expA @ b
        observed = funm_multiply_krylov(expm, A, b)
        assert_allclose_(observed, expected)
        observed = funm_multiply_krylov(expm, aslinearoperator(A), b)
        assert_allclose_(observed, expected)

