
def test_sycon_hecon():
    rng = np.random.default_rng(1234)
    for ind, dtype in enumerate(DTYPES+COMPLEX_DTYPES):
        # DTYPES + COMPLEX DTYPES = <s,d,c,z> sycon + <c,z>hecon
        n = 10
        # For <s,d,c,z>sycon
        if ind < 4:
            func_lwork = get_lapack_funcs('sytrf_lwork', dtype=dtype)
            funcon, functrf = get_lapack_funcs(('sycon', 'sytrf'), dtype=dtype)
            A = (rng.random((n, n))).astype(dtype)
        # For <c,z>hecon
        else:
            func_lwork = get_lapack_funcs('hetrf_lwork', dtype=dtype)
            funcon, functrf = get_lapack_funcs(('hecon', 'hetrf'), dtype=dtype)
            A = (rng.random((n, n)) + rng.random((n, n))*1j).astype(dtype)

        # Since sycon only refers to upper/lower part, conj() is safe here.
        A = (A + A.conj().T)/2 + 2*np.eye(n, dtype=dtype)

        anorm = norm(A, 1)
        lwork = _compute_lwork(func_lwork, n)
        ldu, ipiv, _ = functrf(A, lwork=lwork, lower=1)
        rcond, _ = funcon(a=ldu, ipiv=ipiv, anorm=anorm, lower=1)
        # The error is at most 1-fold
        assert_(abs(1/rcond - np.linalg.cond(A, p=1))*rcond < 1)

