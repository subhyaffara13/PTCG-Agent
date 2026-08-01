
def test_ptsvx_error_raise_errors(dtype, realtype, fact, df_de_lambda):
    rng = np.random.RandomState(42)
    ptsvx = get_lapack_funcs('ptsvx', dtype=dtype)
    n = 5
    # create diagonals according to size and dtype
    d = generate_random_dtype_array((n,), realtype, rng) + 4
    e = generate_random_dtype_array((n-1,), dtype, rng)
    A = np.diag(d) + np.diag(e, -1) + np.diag(np.conj(e), 1)
    x_soln = generate_random_dtype_array((n, 2), dtype=dtype, rng=rng)
    b = A @ x_soln

    # use lambda to determine what df, ef are
    df, ef, info = df_de_lambda(d, e)

    # test with malformatted array sizes
    assert_raises(ValueError, ptsvx, d[:-1], e, b, fact=fact, df=df, ef=ef)
    assert_raises(ValueError, ptsvx, d, e[:-1], b, fact=fact, df=df, ef=ef)
    assert_raises(Exception, ptsvx, d, e, b[:-1], fact=fact, df=df, ef=ef)

