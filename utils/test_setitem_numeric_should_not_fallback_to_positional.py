
def test_setitem_numeric_should_not_fallback_to_positional(any_numeric_dtype):
    # GH51053
    dtype = any_numeric_dtype
    idx = Index([1, 0, 1], dtype=dtype)
    ser = Series(range(3), index=idx)
    ser[1] = 10
    expected = Series([10, 1, 10], index=idx)
    tm.assert_series_equal(ser, expected, check_exact=True)

