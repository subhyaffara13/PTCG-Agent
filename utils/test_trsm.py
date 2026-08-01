
def test_trsm(f, dtype):
    rng = np.random.default_rng(1234)
    tol = np.finfo(dtype).eps*1000
    func = f

    # Test protection against size mismatches
    A = rng.random((4, 5)).astype(dtype)
    B = rng.random((4, 4)).astype(dtype)
    alpha = dtype(1)
    assert_raises(Exception, func, alpha, A, B)
    assert_raises(Exception, func, alpha, A.T, B)

    n = 8
    m = 7
    alpha = dtype(-2.5)
    if dtype in COMPLEX_DTYPES:
        A = (rng.random((m, m)) + rng.random((m, m))*1j) + eye(m)
    else:
        A = rng.random((m, m)) + eye(m)
    A = A.astype(dtype)
    Au = triu(A)
    Al = tril(A)
    B1 = rng.random((m, n)).astype(dtype)
    B2 = rng.random((n, m)).astype(dtype)

    x1 = func(alpha=alpha, a=A, b=B1)
    assert_equal(B1.shape, x1.shape)
    x2 = solve(Au, alpha*B1)
    assert_allclose(x1, x2, atol=tol)

    x1 = func(alpha=alpha, a=A, b=B1, trans_a=1)
    x2 = solve(Au.T, alpha*B1)
    assert_allclose(x1, x2, atol=tol)

    x1 = func(alpha=alpha, a=A, b=B1, trans_a=2)
    x2 = solve(Au.conj().T, alpha*B1)
    assert_allclose(x1, x2, atol=tol)

    x1 = func(alpha=alpha, a=A, b=B1, diag=1)
    Au[arange(m), arange(m)] = dtype(1)
    x2 = solve(Au, alpha*B1)
    assert_allclose(x1, x2, atol=tol)

    x1 = func(alpha=alpha, a=A, b=B2, diag=1, side=1)
    x2 = solve(Au.conj().T, alpha*B2.conj().T)
    assert_allclose(x1, x2.conj().T, atol=tol)

    x1 = func(alpha=alpha, a=A, b=B2, diag=1, side=1, lower=1)
    Al[arange(m), arange(m)] = dtype(1)
    x2 = solve(Al.conj().T, alpha*B2.conj().T)
    assert_allclose(x1, x2.conj().T, atol=tol)

