
def test_tfsm():
    """
    Test for solving a linear system with the coefficient matrix is a
    triangular array stored in Full Packed (RFP) format.
    """
    rng = np.random.RandomState(1234)
    for ind, dtype in enumerate(DTYPES):
        n = 20
        if ind > 1:
            A = triu(rng.rand(n, n) + rng.rand(n, n)*1j + eye(n)).astype(dtype)
            trans = 'C'
        else:
            A = triu(rng.rand(n, n) + eye(n)).astype(dtype)
            trans = 'T'

        trttf, tfttr, tfsm = get_lapack_funcs(('trttf', 'tfttr', 'tfsm'),
                                              dtype=dtype)

        Afp, _ = trttf(A)
        B = rng.rand(n, 2).astype(dtype)
        soln = tfsm(-1, Afp, B)
        assert_array_almost_equal(soln, solve(-A, B),
                                  decimal=4 if ind % 2 == 0 else 6)

        soln = tfsm(-1, Afp, B, trans=trans)
        assert_array_almost_equal(soln, solve(-A.conj().T, B),
                                  decimal=4 if ind % 2 == 0 else 6)

        # Make A, unit diagonal
        A[np.arange(n), np.arange(n)] = dtype(1.)
        soln = tfsm(-1, Afp, B, trans=trans, diag='U')
        assert_array_almost_equal(soln, solve(-A.conj().T, B),
                                  decimal=4 if ind % 2 == 0 else 6)

        # Change side
        B2 = rng.rand(3, n).astype(dtype)
        soln = tfsm(-1, Afp, B2, trans=trans, diag='U', side='R')
        assert_array_almost_equal(soln, solve(-A, B2.T).conj().T,
                                  decimal=4 if ind % 2 == 0 else 6)

