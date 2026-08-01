
def test_sfrk_hfrk():
    """
    Test for performing a symmetric rank-k operation for matrix in RFP format.
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

        prefix = 's'if ind < 2 else 'h'
        trttf, tfttr, shfrk = get_lapack_funcs(('trttf', 'tfttr', f'{prefix}frk'),
                                               dtype=dtype)

        Afp, _ = trttf(A)
        C = rng.rand(n, 2).astype(dtype)
        Afp_out = shfrk(n, 2, -1, C, 2, Afp)
        A_out, _ = tfttr(n, Afp_out)
        assert_array_almost_equal(A_out, triu(-C.dot(C.conj().T) + 2*A),
                                  decimal=4 if ind % 2 == 0 else 6)

