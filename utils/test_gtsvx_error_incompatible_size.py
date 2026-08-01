
def test_gtsvx_error_incompatible_size(dtype, trans_bool, fact):
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

    if fact == "N":
        assert_raises(ValueError, gtsvx, dl[:-1], d, du, b,
                      fact=fact, trans=trans, dlf=dlf_, df=df_,
                      duf=duf_, du2=du2f_, ipiv=ipiv_)
        assert_raises(ValueError, gtsvx, dl, d[:-1], du, b,
                      fact=fact, trans=trans, dlf=dlf_, df=df_,
                      duf=duf_, du2=du2f_, ipiv=ipiv_)
        assert_raises(ValueError, gtsvx, dl, d, du[:-1], b,
                      fact=fact, trans=trans, dlf=dlf_, df=df_,
                      duf=duf_, du2=du2f_, ipiv=ipiv_)
        assert_raises(Exception, gtsvx, dl, d, du, b[:-1],
                      fact=fact, trans=trans, dlf=dlf_, df=df_,
                      duf=duf_, du2=du2f_, ipiv=ipiv_)
    else:
        assert_raises(ValueError, gtsvx, dl, d, du, b,
                      fact=fact, trans=trans, dlf=dlf_[:-1], df=df_,
                      duf=duf_, du2=du2f_, ipiv=ipiv_)
        assert_raises(ValueError, gtsvx, dl, d, du, b,
                      fact=fact, trans=trans, dlf=dlf_, df=df_[:-1],
                      duf=duf_, du2=du2f_, ipiv=ipiv_)
        assert_raises(ValueError, gtsvx, dl, d, du, b,
                      fact=fact, trans=trans, dlf=dlf_, df=df_,
                      duf=duf_[:-1], du2=du2f_, ipiv=ipiv_)
        assert_raises(ValueError, gtsvx, dl, d, du, b,
                      fact=fact, trans=trans, dlf=dlf_, df=df_,
                      duf=duf_, du2=du2f_[:-1], ipiv=ipiv_)

