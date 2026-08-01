
def test_getitem_str_month_with_datetimeindex():
    # GH3546 (not including times on the last day)
    idx = date_range(start="2013-05-31 00:00", end="2013-05-31 23:00", freq="h")
    ts = Series(range(len(idx)), index=idx)
    expected = ts["2013-05"]
    tm.assert_series_equal(expected, ts)

    idx = date_range(start="2013-05-31 00:00", end="2013-05-31 23:59", freq="s")
    ts = Series(range(len(idx)), index=idx)
    expected = ts["2013-05"]
    tm.assert_series_equal(expected, ts)

