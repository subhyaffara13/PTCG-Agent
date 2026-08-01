
def test_pftrf():
    """
    Test Cholesky factorization of a positive definite Rectangular Full
    Packed (RFP) format array
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

        pftrf, trttf, tfttr = get_lapack_funcs(('pftrf', 'trttf', 'tfttr'),
                                               dtype=dtype)

        # Get the original array from TP
        Afp, info = trttf(A)
        Achol_rfp, info = pftrf(n, Afp)
        assert_(info == 0)
        A_chol_r, _ = tfttr(n, Achol_rfp)
        Achol = cholesky(A)
        assert_array_almost_equal(A_chol_r, Achol)

