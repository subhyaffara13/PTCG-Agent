
def test_float_index(temp_h5_path):
    # GH #454
    index = np.random.default_rng(2).standard_normal(10)
    s = Series(np.random.default_rng(2).standard_normal(10), index=index)
    _check_roundtrip(s, tm.assert_series_equal, path=temp_h5_path)

