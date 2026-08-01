
def test_getitem_str_year_with_datetimeindex():
    idx = [
        Timestamp("2013-05-31 00:00"),
        Timestamp(datetime(2013, 5, 31, 23, 59, 59, 999999)),
    ]
    ts = Series(range(len(idx)), index=idx)
    expected = ts["2013"]
    tm.assert_series_equal(expected, ts)

