
def test_closed_median_quantile(closed, expected):
    # GH 26005
    ser = Series(data=np.arange(10), index=date_range("2000", periods=10))
    roll = ser.rolling("3D", closed=closed)
    expected = Series(expected, index=ser.index)

    result = roll.median()
    tm.assert_series_equal(result, expected)

    result = roll.quantile(0.5)
    tm.assert_series_equal(result, expected)

