
def test_get_dir_vector(zdir, expected):
    res = get_dir_vector(zdir)
    assert isinstance(res, np.ndarray)
    nptest.assert_array_equal(res, expected)

