
def test_closed_min_max_minp(func, closed, expected):
    # see gh-21704
    ser = Series(data=np.arange(10), index=date_range("2000", periods=10))
    # Explicit cast to float to avoid implicit cast when setting nan
    ser = ser.astype("float")
    ser[ser.index[-3:]] = np.nan
    result = getattr(ser.rolling("3D", min_periods=2, closed=closed), func)()
    expected = Series(expected, index=ser.index)
    tm.assert_series_equal(result, expected)

