
def test_ptsvx(dtype, realtype, fact, df_de_lambda):
    '''
    This tests the ?ptsvx lapack routine wrapper to solve a random system
    Ax = b for all dtypes and input variations. Tests for: unmodified
    input parameters, fact options, incompatible matrix shapes raise an error,
    and singular matrices return info of illegal value.
    '''
    rng = np.random.RandomState(42)
    # set test tolerance appropriate for dtype
    atol = 100 * np.finfo(dtype).eps
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

    # create copy to later test that they are unmodified
    diag_cpy = [d.copy(), e.copy(), b.copy()]

    # solve using routine
    df, ef, x, rcond, ferr, berr, info = ptsvx(d, e, b, fact=fact,
                                               df=df, ef=ef)
    # d, e, and b should be unmodified
    assert_array_equal(d, diag_cpy[0])
    assert_array_equal(e, diag_cpy[1])
    assert_array_equal(b, diag_cpy[2])
    assert_(info == 0, f"info should be 0 but is {info}.")
    assert_array_almost_equal(x_soln, x)

    # test that the factors from ptsvx can be recombined to make A
    L = np.diag(ef, -1) + np.diag(np.ones(n))
    D = np.diag(df)
    assert_allclose(A, L@D@(np.conj(L).T), atol=atol)

    # assert that the outputs are of correct type or shape
    # rcond should be a scalar
    assert not hasattr(rcond, "__len__"), \
        f"rcond should be scalar but is {rcond}"
    # ferr should be length of # of cols in x
    assert_(ferr.shape == (2,), (f"ferr.shape is {ferr.shape} but should be "
                                 "({x_soln.shape[1]},)"))
    # berr should be length of # of cols in x
    assert_(berr.shape == (2,), (f"berr.shape is {berr.shape} but should be "
                                 "({x_soln.shape[1]},)"))

