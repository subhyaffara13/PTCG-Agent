
def test_geqrf_lwork(dtype, shape):
    geqrf_lwork = get_lapack_funcs(('geqrf_lwork'), dtype=dtype)
    m, n = shape
    lwork, info = geqrf_lwork(m=m, n=n)
    assert_equal(info, 0)

