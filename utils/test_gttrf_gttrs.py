
def test_gttrf_gttrs(dtype):
    # The test uses ?gttrf and ?gttrs to solve a random system for each dtype,
    # tests that the output of ?gttrf define LU matrices, that input
    # parameters are unmodified, transposal options function correctly, that
    # incompatible matrix shapes raise an error, and singular matrices return
    # non zero info.

    rng = np.random.RandomState(42)
    n = 10
    atol = 100 * np.finfo(dtype).eps

    # create the matrix in accordance with the data type
    du = generate_random_dtype_array((n-1,), dtype=dtype, rng=rng)
    d = generate_random_dtype_array((n,), dtype=dtype, rng=rng)
    dl = generate_random_dtype_array((n-1,), dtype=dtype, rng=rng)

    diag_cpy = [dl.copy(), d.copy(), du.copy()]

    A = np.diag(d) + np.diag(dl, -1) + np.diag(du, 1)
    x = rng.random(n)
    b = A @ x

    gttrf, gttrs = get_lapack_funcs(('gttrf', 'gttrs'), dtype=dtype)

    _dl, _d, _du, du2, ipiv, info = gttrf(dl, d, du)
    # test to assure that the inputs of ?gttrf are unmodified
    assert_array_equal(dl, diag_cpy[0])
    assert_array_equal(d, diag_cpy[1])
    assert_array_equal(du, diag_cpy[2])

    # generate L and U factors from ?gttrf return values
    # L/U are lower/upper triangular by construction (initially and at end)
    U = np.diag(_d, 0) + np.diag(_du, 1) + np.diag(du2, 2)
    L = np.eye(n, dtype=dtype)

    for i, m in enumerate(_dl):
        # L is given in a factored form.
        # See
        # www.hpcavf.uclan.ac.uk/softwaredoc/sgi_scsl_html/sgi_html/ch03.html
        piv = ipiv[i] - 1
        # right multiply by permutation matrix
        L[:, [i, piv]] = L[:, [piv, i]]
        # right multiply by Li, rank-one modification of identity
        L[:, i] += L[:, i+1]*m

    # one last permutation
    i, piv = -1, ipiv[-1] - 1
    # right multiply by final permutation matrix
    L[:, [i, piv]] = L[:, [piv, i]]

    # check that the outputs of ?gttrf define an LU decomposition of A
    assert_allclose(A, L @ U, atol=atol)

    b_cpy = b.copy()
    x_gttrs, info = gttrs(_dl, _d, _du, du2, ipiv, b)
    # test that the inputs of ?gttrs are unmodified
    assert_array_equal(b, b_cpy)
    # test that the result of ?gttrs matches the expected input
    assert_allclose(x, x_gttrs, atol=atol)

    # test that ?gttrf and ?gttrs work with transposal options
    if dtype in REAL_DTYPES:
        trans = "T"
        b_trans = A.T @ x
    else:
        trans = "C"
        b_trans = A.conj().T @ x

    x_gttrs, info = gttrs(_dl, _d, _du, du2, ipiv, b_trans, trans=trans)
    assert_allclose(x, x_gttrs, atol=atol)

    # test that ValueError is raised with incompatible matrix shapes
    with assert_raises(ValueError):
        gttrf(dl[:-1], d, du)
    with assert_raises(ValueError):
        gttrf(dl, d[:-1], du)
    with assert_raises(ValueError):
        gttrf(dl, d, du[:-1])

    # test that matrix of size n=2 raises exception
    with assert_raises(ValueError):
        gttrf(dl[0], d[:1], du[0])

    # test that singular (row of all zeroes) matrix fails via info
    du[0] = 0
    d[0] = 0
    __dl, __d, __du, _du2, _ipiv, _info = gttrf(dl, d, du)
    np.testing.assert_(__d[info - 1] == 0, (f"?gttrf: _d[info-1] is {__d[info - 1]},"
                                            " not the illegal value :0."))

