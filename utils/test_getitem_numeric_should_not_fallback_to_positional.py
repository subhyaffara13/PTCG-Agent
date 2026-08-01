
def test_getitem_numeric_should_not_fallback_to_positional(any_numeric_dtype):
    # GH51053
    dtype = any_numeric_dtype
    idx = Index([1, 0, 1], dtype=dtype)
    ser = Series(range(3), index=idx)
    result = ser[1]
    expected = Series([0, 2], index=Index([1, 1], dtype=dtype))
    tm.assert_series_equal(result, expected, check_exact=True)

