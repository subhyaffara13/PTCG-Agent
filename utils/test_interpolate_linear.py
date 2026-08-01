
def test_interpolate_linear(dtype):
    ser = pd.Series([None, 1, 2, None, 4, None], dtype=dtype)
    result = ser.interpolate()
    expected = pd.Series([None, 1, 2, 3, 4, None], dtype=dtype)
    tm.assert_series_equal(result, expected)

