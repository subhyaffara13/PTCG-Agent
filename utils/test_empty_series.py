
def test_empty_series(dtype, temp_h5_path):
    s = Series(dtype=dtype)
    _check_roundtrip(s, tm.assert_series_equal, path=temp_h5_path)

