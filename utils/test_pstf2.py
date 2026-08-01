
def test_pstf2():
    rng = np.random.RandomState(1234)
    for ind, dtype in enumerate(DTYPES):
        # DTYPES = <s, d, c, z> pstf2
        n = 10
        r = 2
        pstf2 = get_lapack_funcs('pstf2', dtype=dtype)

        # Create positive semidefinite A
        if ind > 1:
            A = rng.rand(n, n-r).astype(dtype) + 1j * rng.rand(n, n-r).astype(dtype)
            A = A @ A.conj().T
        else:
            A = rng.rand(n, n-r).astype(dtype)
            A = A @ A.T

        c, piv, r_c, info = pstf2(A)
        U = triu(c)
        U[r_c - n:, r_c - n:] = 0.

        assert_equal(info, 1)
        # python-dbg 3.5.2 runs cause trouble with the commented assertions.
        # assert_equal(r_c, n - r)
        single_atol = 1000 * np.finfo(np.float32).eps
        double_atol = 1000 * np.finfo(np.float64).eps
        atol = single_atol if ind in [0, 2] else double_atol
        assert_allclose(A[piv-1][:, piv-1], U.conj().T @ U, rtol=0., atol=atol)

        c, piv, r_c, info = pstf2(A, lower=1)
        L = tril(c)
        L[r_c - n:, r_c - n:] = 0.

        assert_equal(info, 1)
        # assert_equal(r_c, n - r)
        single_atol = 1000 * np.finfo(np.float32).eps
        double_atol = 1000 * np.finfo(np.float64).eps
        atol = single_atol if ind in [0, 2] else double_atol
        assert_allclose(A[piv-1][:, piv-1], L @ L.conj().T, rtol=0., atol=atol)

