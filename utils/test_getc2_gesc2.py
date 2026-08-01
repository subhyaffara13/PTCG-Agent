
def test_getc2_gesc2():
    rng = np.random.RandomState(42)
    n = 10
    desired_real = rng.rand(n)
    desired_cplx = rng.rand(n) + rng.rand(n)*1j

    for ind, dtype in enumerate(DTYPES):
        if ind < 2:
            A = rng.rand(n, n)
            A = A.astype(dtype)
            b = A @ desired_real
            b = b.astype(dtype)
        else:
            A = rng.rand(n, n) + rng.rand(n, n)*1j
            A = A.astype(dtype)
            b = A @ desired_cplx
            b = b.astype(dtype)

        getc2 = get_lapack_funcs('getc2', dtype=dtype)
        gesc2 = get_lapack_funcs('gesc2', dtype=dtype)
        lu, ipiv, jpiv, info = getc2(A, overwrite_a=0)
        x, scale = gesc2(lu, b, ipiv, jpiv, overwrite_rhs=0)

        if ind < 2:
            assert_array_almost_equal(desired_real.astype(dtype),
                                      x/scale, decimal=4)
        else:
            assert_array_almost_equal(desired_cplx.astype(dtype),
                                      x/scale, decimal=4)

