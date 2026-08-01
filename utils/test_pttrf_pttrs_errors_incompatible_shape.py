
def test_pttrf_pttrs_errors_incompatible_shape(ddtype, dtype):
    n = 10
    rng = np.random.RandomState(1234)
    pttrf = get_lapack_funcs('pttrf', dtype=dtype)
    d = generate_random_dtype_array((n,), ddtype, rng) + 2
    e = generate_random_dtype_array((n-1,), dtype, rng)
    # test that ValueError is raised with incompatible matrix shapes
    assert_raises(ValueError, pttrf, d[:-1], e)
    assert_raises(ValueError, pttrf, d, e[:-1])

