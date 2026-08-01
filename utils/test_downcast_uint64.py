
def test_downcast_uint64():
    # see gh-14422:
    # BUG: to_numeric doesn't work uint64 numbers
    ser = Series([0, 9223372036854775808])
    result = to_numeric(ser, downcast="unsigned")
    expected = Series([0, 9223372036854775808], dtype=np.uint64)
    tm.assert_series_equal(result, expected)

