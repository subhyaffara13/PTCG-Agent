
def test_iter_rolling_datetime(expected, expected_index, window):
    # GH 11704
    ser = Series(range(5), index=date_range(start="2020-01-01", periods=5, freq="D"))

    expecteds = [
        Series(values, index=idx)
        for (values, idx) in zip(expected, expected_index, strict=True)
    ]

    for expected, actual in zip(expecteds, ser.rolling(window), strict=True):
        tm.assert_series_equal(actual, expected)

