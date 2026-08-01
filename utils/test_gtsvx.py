
def test_gtsvx(dtype, trans_bool, fact):
    """
    These tests uses ?gtsvx to solve a random Ax=b system for each dtype.
    It tests that the outputs define an LU matrix, that inputs are unmodified,
    transposal options, incompatible shapes, singular matrices, and
    singular factorizations. It parametrizes DTYPES and the 'fact' value along
    with the fact related inputs.
    """
    rng = np.random.RandomState(42)
    # set test tolerance appropriate for dtype
    atol = 100 * np.finfo(dtype).eps
    # obtain routine
    gtsvx, gttrf = get_lapack_funcs(('gtsvx', 'gttrf'), dtype=dtype)
    # Generate random tridiagonal matrix A
    n = 10
    dl = generate_random_dtype_array((n-1,), dtype=dtype, rng=rng)
    d = generate_random_dtype_array((n,), dtype=dtype, rng=rng)
    du = generate_random_dtype_array((n-1,), dtype=dtype, rng=rng)
    A = np.diag(dl, -1) + np.diag(d) + np.diag(du, 1)
    # generate random solution x
    x = generate_random_dtype_array((n, 2), dtype=dtype, rng=rng)
    # create b from x for equation Ax=b
    trans = ("T" if dtype in REAL_DTYPES else "C") if trans_bool else "N"
    b = (A.conj().T if trans_bool else A) @ x

    # store a copy of the inputs to check they haven't been modified later
    inputs_cpy = [dl.copy(), d.copy(), du.copy(), b.copy()]

    # set these to None if fact = 'N', or the output of gttrf is fact = 'F'
    dlf_, df_, duf_, du2f_, ipiv_, info_ = \
        gttrf(dl, d, du) if fact == 'F' else [None]*6

    gtsvx_out = gtsvx(dl, d, du, b, fact=fact, trans=trans, dlf=dlf_, df=df_,
                      duf=duf_, du2=du2f_, ipiv=ipiv_)
    dlf, df, duf, du2f, ipiv, x_soln, rcond, ferr, berr, info = gtsvx_out
    assert_(info == 0, f"?gtsvx info = {info}, should be zero")

    # assure that inputs are unmodified
    assert_array_equal(dl, inputs_cpy[0])
    assert_array_equal(d, inputs_cpy[1])
    assert_array_equal(du, inputs_cpy[2])
    assert_array_equal(b, inputs_cpy[3])

    # test that x_soln matches the expected x
    assert_allclose(x, x_soln, atol=atol)

    # assert that the outputs are of correct type or shape
    # rcond should be a scalar
    assert_(hasattr(rcond, "__len__") is not True,
            f"rcond should be scalar but is {rcond}")
    # ferr should be length of # of cols in x
    assert_(ferr.shape[0] == b.shape[1], (f"ferr.shape is {ferr.shape[0]} but should"
                                          f" be {b.shape[1]}"))
    # berr should be length of # of cols in x
    assert_(berr.shape[0] == b.shape[1], (f"berr.shape is {berr.shape[0]} but should"
                                          f" be {b.shape[1]}"))

