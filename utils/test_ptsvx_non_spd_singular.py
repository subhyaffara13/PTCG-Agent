
def test_ptsvx_non_SPD_singular(dtype, realtype, fact, df_de_lambda):
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

    if fact == "N":
        d[3] = 0
        # obtain new df, ef
        df, ef, info = df_de_lambda(d, e)
        # solve using routine
        df, ef, x, rcond, ferr, berr, info = ptsvx(d, e, b)
        # test for the singular matrix.
        assert info > 0 and info <= n

        # non SPD matrix
        d = generate_random_dtype_array((n,), realtype, rng)
        df, ef, x, rcond, ferr, berr, info = ptsvx(d, e, b)
        assert info > 0 and info <= n
    else:
        # assuming that someone is using a singular factorization
        df, ef, info = df_de_lambda(d, e)
        df[0] = 0
        ef[0] = 0
        df, ef, x, rcond, ferr, berr, info = ptsvx(d, e, b, fact=fact,
                                                   df=df, ef=ef)
        assert info > 0

