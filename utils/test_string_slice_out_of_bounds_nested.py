
def test_string_slice_out_of_bounds_nested():
    ser = Series([(1, 2), (1,), (3, 4, 5)])
    result = ser.str[1]
    expected = Series([2, np.nan, 4])
    tm.assert_series_equal(result, expected)

