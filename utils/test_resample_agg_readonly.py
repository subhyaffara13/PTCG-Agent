
def test_resample_agg_readonly():
    # GH#31710 cython needs to allow readonly data
    index = date_range("2020-01-01", "2020-01-02", freq="1h", unit="ns")
    arr = np.zeros_like(index)
    arr.setflags(write=False)

    ser = Series(arr, index=index)
    rs = ser.resample("1D")

    expected = Series([pd.Timestamp(0), pd.Timestamp(0)], index=index[::24])
    expected.index.freq = Day(1)  # GH#41943 no longer equivalent to 24h

    result = rs.agg("last")
    tm.assert_series_equal(result, expected)

    result = rs.agg("first")
    tm.assert_series_equal(result, expected)

    result = rs.agg("max")
    tm.assert_series_equal(result, expected)

    result = rs.agg("min")
    tm.assert_series_equal(result, expected)

