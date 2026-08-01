
def test_upsample_sum(method, method_args, expected_values):
    ser = Series(1, index=date_range("2017", periods=2, freq="h", unit="ns"))
    resampled = ser.resample("30min")
    index = pd.DatetimeIndex(
        ["2017-01-01T00:00:00", "2017-01-01T00:30:00", "2017-01-01T01:00:00"],
        dtype="M8[ns]",
        freq="30min",
    )
    result = methodcaller(method, **method_args)(resampled)
    expected = Series(expected_values, index=index)
    tm.assert_series_equal(result, expected)

