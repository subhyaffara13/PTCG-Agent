
def test_geqrfp_errors_with_empty_array():
    # check that empty array raises good error message
    A_empty = np.array([])
    geqrfp = get_lapack_funcs('geqrfp', dtype=A_empty.dtype)
    assert_raises(Exception, geqrfp, A_empty)

