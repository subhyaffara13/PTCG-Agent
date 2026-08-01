
def test_iter_rolling_series(ser, expected, window, min_periods):
    # GH 11704
    expecteds = [Series(values, index=index) for (values, index) in expected]

    for expected, actual in zip(
        expecteds, ser.rolling(window, min_periods=min_periods), strict=True
    ):
        tm.assert_series_equal(actual, expected)

