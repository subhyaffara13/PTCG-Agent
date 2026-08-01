
def test_rolling_skew_kurt_numerical_stability(method):
    # GH#6929
    ser = Series(np.random.default_rng(2).random(10))
    ser_copy = ser.copy()
    expected = getattr(ser.rolling(3), method)()
    tm.assert_series_equal(ser, ser_copy)
    ser = ser + 50000
    result = getattr(ser.rolling(3), method)()
    tm.assert_series_equal(result, expected)

