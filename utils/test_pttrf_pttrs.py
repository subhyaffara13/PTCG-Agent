
def test_pttrf_pttrs(ddtype, dtype):
    rng = np.random.RandomState(42)
    # set test tolerance appropriate for dtype
    atol = 100*np.finfo(dtype).eps
    # n is the length diagonal of A
    n = 10
    # create diagonals according to size and dtype

    # diagonal d should always be real.
    # add 4 to d so it will be dominant for all dtypes
    d = generate_random_dtype_array((n,), ddtype, rng) + 4
    # diagonal e may be real or complex.
    e = generate_random_dtype_array((n-1,), dtype, rng)

    # assemble diagonals together into matrix
    A = np.diag(d) + np.diag(e, -1) + np.diag(np.conj(e), 1)
    # store a copy of diagonals to later verify
    diag_cpy = [d.copy(), e.copy()]

    pttrf = get_lapack_funcs('pttrf', dtype=dtype)

    _d, _e, info = pttrf(d, e)
    # test to assure that the inputs of ?pttrf are unmodified
    assert_array_equal(d, diag_cpy[0])
    assert_array_equal(e, diag_cpy[1])
    assert_equal(info, 0, err_msg=f"pttrf: info = {info}, should be 0")

    # test that the factors from pttrf can be recombined to make A
    L = np.diag(_e, -1) + np.diag(np.ones(n))
    D = np.diag(_d)

    assert_allclose(A, L@D@L.conjugate().T, atol=atol)

    # generate random solution x
    x = generate_random_dtype_array((n,), dtype, rng)
    # determine accompanying b to get soln x
    b = A@x

    # determine _x from pttrs
    pttrs = get_lapack_funcs('pttrs', dtype=dtype)
    _x, info = pttrs(_d, _e.conj(), b)
    assert_equal(info, 0, err_msg=f"pttrs: info = {info}, should be 0")

    # test that _x from pttrs matches the expected x
    assert_allclose(x, _x, atol=atol)

