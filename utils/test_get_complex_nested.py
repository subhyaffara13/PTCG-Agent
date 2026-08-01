
def test_get_complex_nested(to_type):
    ser = Series([to_type([to_type([1, 2])])])

    result = ser.str.get(0)
    expected = Series([to_type([1, 2])])
    tm.assert_series_equal(result, expected)

    result = ser.str.get(1)
    expected = Series([np.nan])
    tm.assert_series_equal(result, expected)

