
def test_pttrf_pttrs_errors_singular_nonSPD(ddtype, dtype):
    n = 10
    rng = np.random.RandomState(42)
    pttrf = get_lapack_funcs('pttrf', dtype=dtype)
    d = generate_random_dtype_array((n,), ddtype, rng) + 2
    e = generate_random_dtype_array((n-1,), dtype, rng)
    # test that singular (row of all zeroes) matrix fails via info
    d[0] = 0
    e[0] = 0
    _d, _e, info = pttrf(d, e)
    assert_equal(_d[info - 1], 0,
                 f"?pttrf: _d[info-1] is {_d[info - 1]}, not the illegal value :0.")

    # test with non-spd matrix
    d = generate_random_dtype_array((n,), ddtype, rng)
    _d, _e, info = pttrf(d, e)
    assert_(info != 0, "?pttrf should fail with non-spd matrix, but didn't")

