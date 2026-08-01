
def test_series_set_value(using_infer_string):
    # GH#1561, GH#51363 as of 3.0 we do not do inference in Index.insert

    dates = [datetime(2001, 1, 1), datetime(2001, 1, 2)]
    if using_infer_string:
        index = DatetimeIndex(dates)
    else:
        index = Index(dates, dtype=object)

    s = Series(dtype=object)
    s._set_value(dates[0], 1.0)
    s._set_value(dates[1], np.nan)

    expected = Series([1.0, np.nan], index=index)

    tm.assert_series_equal(s, expected)

