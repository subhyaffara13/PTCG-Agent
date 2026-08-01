
def test_syconv():
    """
    Test for going back and forth between the returned format of he/sytrf to
    L and D factors/permutations.
    """
    rng = np.random.RandomState(1234)
    for ind, dtype in enumerate(DTYPES):
        n = 10

        if ind > 1:
            A = (rng.randint(-30, 30, (n, n)) +
                 rng.randint(-30, 30, (n, n))*1j).astype(dtype)

            A = A + A.conj().T
        else:
            A = rng.randint(-30, 30, (n, n)).astype(dtype)
            A = A + A.T + n*eye(n)

        tol = 100*np.spacing(dtype(1.0).real)
        syconv, trf, trf_lwork = get_lapack_funcs(('syconv', 'sytrf',
                                                   'sytrf_lwork'), dtype=dtype)
        lw = _compute_lwork(trf_lwork, n, lower=1)
        L, D, perm = ldl(A, lower=1, hermitian=False)
        lw = _compute_lwork(trf_lwork, n, lower=1)
        ldu, ipiv, info = trf(A, lower=1, lwork=lw)
        a, e, info = syconv(ldu, ipiv, lower=1)
        assert_allclose(tril(a, -1,), tril(L[perm, :], -1), atol=tol, rtol=0.)

        # Test also upper
        U, D, perm = ldl(A, lower=0, hermitian=False)
        ldu, ipiv, info = trf(A, lower=0)
        a, e, info = syconv(ldu, ipiv, lower=0)
        assert_allclose(triu(a, 1), triu(U[perm, :], 1), atol=tol, rtol=0.)

