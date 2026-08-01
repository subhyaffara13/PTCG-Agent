
def test_string_slice_out_of_bounds(any_string_dtype):
    ser = Series(["foo", "b", "ba"], dtype=any_string_dtype)
    result = ser.str[1]
    expected = Series(["o", np.nan, "a"], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

