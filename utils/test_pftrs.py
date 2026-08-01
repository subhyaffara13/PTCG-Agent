
def test_pftrs():
    """
    Test Cholesky factorization of a positive definite Rectangular Full
    Packed (RFP) format array and solve a linear system
    """
    rng = np.random.RandomState(1234)
    for ind, dtype in enumerate(DTYPES):
        n = 20
        if ind > 1:
            A = (rng.rand(n, n) + rng.rand(n, n)*1j).astype(dtype)
            A = A + A.conj().T + n*eye(n)
        else:
            A = (rng.rand(n, n)).astype(dtype)
            A = A + A.T + n*eye(n)

        B = ones((n, 3), dtype=dtype)
        Bf1 = ones((n+2, 3), dtype=dtype)
        Bf2 = ones((n-2, 3), dtype=dtype)
        pftrs, pftrf, trttf, tfttr = get_lapack_funcs(('pftrs',
                                                       'pftrf',
                                                       'trttf',
                                                       'tfttr'),
                                                      dtype=dtype)

        # Get the original array from TP
        Afp, info = trttf(A)
        A_chol_rfp, info = pftrf(n, Afp)
        # larger B arrays shouldn't segfault
        soln, info = pftrs(n, A_chol_rfp, Bf1)
        assert_(info == 0)
        assert_raises(Exception, pftrs, n, A_chol_rfp, Bf2)
        soln, info = pftrs(n, A_chol_rfp, B)
        assert_(info == 0)
        assert_array_almost_equal(solve(A, B), soln,
                                  decimal=4 if ind % 2 == 0 else 6)

