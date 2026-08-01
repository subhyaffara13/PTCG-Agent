
def test_tpttr_trttp():
    """
    Test conversion routines between the Rectangular Full Packed (RFP) format
    and Standard Triangular Array (TR)
    """
    rng = np.random.RandomState(1234)
    for ind, dtype in enumerate(DTYPES):
        n = 20
        if ind > 1:
            A_full = (rng.rand(n, n) + rng.rand(n, n)*1j).astype(dtype)
        else:
            A_full = (rng.rand(n, n)).astype(dtype)

        trttp, tpttr = get_lapack_funcs(('trttp', 'tpttr'), dtype=dtype)
        A_tp_U, info = trttp(A_full)
        assert_(info == 0)
        A_tp_L, info = trttp(A_full, uplo='L')
        assert_(info == 0)

        # Create the TP array manually
        inds = tril_indices(n)
        A_tp_U_m = zeros(n*(n+1)//2, dtype=dtype)
        A_tp_U_m[:] = (triu(A_full).T)[inds]

        inds = triu_indices(n)
        A_tp_L_m = zeros(n*(n+1)//2, dtype=dtype)
        A_tp_L_m[:] = (tril(A_full).T)[inds]

        assert_array_almost_equal(A_tp_U, A_tp_U_m)
        assert_array_almost_equal(A_tp_L, A_tp_L_m)

        # Get the original array from TP
        A_tr_U, info = tpttr(n, A_tp_U)
        assert_(info == 0)
        A_tr_L, info = tpttr(n, A_tp_L, uplo='L')
        assert_(info == 0)

        assert_array_almost_equal(A_tr_U, triu(A_full))
        assert_array_almost_equal(A_tr_L, tril(A_full))

