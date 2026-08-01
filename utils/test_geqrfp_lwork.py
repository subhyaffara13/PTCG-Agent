
def test_geqrfp_lwork(dtype, shape):
    geqrfp_lwork = get_lapack_funcs(('geqrfp_lwork'), dtype=dtype)
    m, n = shape
    lwork, info = geqrfp_lwork(m=m, n=n)
    assert_equal(info, 0)

