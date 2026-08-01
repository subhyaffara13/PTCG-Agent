
def test_iter_expanding_series(ser, expected, min_periods):
    # GH 11704
    expecteds = [Series(values, index=index) for (values, index) in expected]

    for expected, actual in zip(expecteds, ser.expanding(min_periods), strict=True):
        tm.assert_series_equal(actual, expected)

