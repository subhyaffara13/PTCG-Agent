
def test_sygst():
    rng = np.random.default_rng(1234)
    for ind, dtype in enumerate(REAL_DTYPES):
        # DTYPES = <s,d> sygst
        n = 10

        potrf, sygst, syevd, sygvd = get_lapack_funcs(('potrf', 'sygst',
                                                       'syevd', 'sygvd'),
                                                      dtype=dtype)

        A = rng.random((n, n)).astype(dtype)
        A = (A + A.T)/2
        # B must be positive definite
        B = rng.random((n, n)).astype(dtype)
        B = (B + B.T)/2 + 2 * np.eye(n, dtype=dtype)

        # Perform eig (sygvd)
        eig_gvd, _, info = sygvd(A, B)
        assert_(info == 0)

        # Convert to std problem potrf
        b, info = potrf(B)
        assert_(info == 0)
        a, info = sygst(A, b)
        assert_(info == 0)

        eig, _, info = syevd(a)
        assert_(info == 0)
        assert_allclose(eig, eig_gvd, rtol=1.2e-4)

