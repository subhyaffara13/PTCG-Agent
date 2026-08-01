
def test_assert_series_equal_ignore_extension_dtype_mismatch_cross_class():
    # https://github.com/pandas-dev/pandas/issues/35715
    left = Series([1, 2, 3], dtype="Int64")
    right = Series([1, 2, 3], dtype="int64")
    tm.assert_series_equal(left, right, check_dtype=False)

