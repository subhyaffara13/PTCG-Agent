
def test_pftri():
    """
    Test Cholesky factorization of a positive definite Rectangular Full
    Packed (RFP) format array to find its inverse
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

        pftri, pftrf, trttf, tfttr = get_lapack_funcs(('pftri',
                                                       'pftrf',
                                                       'trttf',
                                                       'tfttr'),
                                                      dtype=dtype)

        # Get the original array from TP
        Afp, info = trttf(A)
        A_chol_rfp, info = pftrf(n, Afp)
        A_inv_rfp, info = pftri(n, A_chol_rfp)
        assert_(info == 0)
        A_inv_r, _ = tfttr(n, A_inv_rfp)
        Ainv = inv(A)
        assert_array_almost_equal(A_inv_r, triu(Ainv),
                                  decimal=4 if ind % 2 == 0 else 6)

