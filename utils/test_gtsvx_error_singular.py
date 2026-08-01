
def test_gtsvx_error_singular(dtype, trans_bool, fact):
    rng = np.random.RandomState(42)
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
    trans = "T" if dtype in REAL_DTYPES else "C"
    b = (A.conj().T if trans_bool else A) @ x

    # set these to None if fact = 'N', or the output of gttrf is fact = 'F'
    dlf_, df_, duf_, du2f_, ipiv_, info_ = \
        gttrf(dl, d, du) if fact == 'F' else [None]*6

    gtsvx_out = gtsvx(dl, d, du, b, fact=fact, trans=trans, dlf=dlf_, df=df_,
                      duf=duf_, du2=du2f_, ipiv=ipiv_)
    dlf, df, duf, du2f, ipiv, x_soln, rcond, ferr, berr, info = gtsvx_out
    # test with singular matrix
    # no need to test inputs with fact "F" since ?gttrf already does.
    if fact == "N":
        # Construct a singular example manually
        d[-1] = 0
        dl[-1] = 0
        # solve using routine
        gtsvx_out = gtsvx(dl, d, du, b)
        dlf, df, duf, du2f, ipiv, x_soln, rcond, ferr, berr, info = gtsvx_out
        # test for the singular matrix.
        assert info > 0, "info should be > 0 for singular matrix"

    elif fact == 'F':
        # assuming that a singular factorization is input
        df_[-1] = 0
        duf_[-1] = 0
        du2f_[-1] = 0

        gtsvx_out = gtsvx(dl, d, du, b, fact=fact, dlf=dlf_, df=df_, duf=duf_,
                          du2=du2f_, ipiv=ipiv_)
        dlf, df, duf, du2f, ipiv, x_soln, rcond, ferr, berr, info = gtsvx_out
        # info should not be zero and should provide index of illegal value
        assert info > 0, "info should be > 0 for singular matrix"

