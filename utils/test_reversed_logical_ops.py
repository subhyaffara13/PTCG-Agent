
def test_reversed_logical_ops(any_string_dtype):
    # GH#60234
    dtype = any_string_dtype
    warn = None if dtype == object else Pandas4Warning
    left = Series([True, False, False, True])
    right = Series(["", "", "b", "c"], dtype=dtype)

    msg = "operations between boolean dtype and"
    with tm.assert_produces_warning(warn, match=msg):
        result = left | right
    expected = left | right.astype(bool)
    tm.assert_series_equal(result, expected)

    with tm.assert_produces_warning(warn, match=msg):
        result = left & right
    expected = left & right.astype(bool)
    tm.assert_series_equal(result, expected)

    with tm.assert_produces_warning(warn, match=msg):
        result = left ^ right
    expected = left ^ right.astype(bool)
    tm.assert_series_equal(result, expected)

