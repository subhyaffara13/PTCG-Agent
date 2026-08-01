
def test_datetime_tz_cut(bins, box):
    # see gh-19872
    tz = "US/Eastern"
    ser = Series(date_range("20130101", periods=3, tz=tz, unit="ns"))

    if not isinstance(bins, int):
        bins = box(bins)

    result = cut(ser, bins)
    ii = IntervalIndex(
        [
            Interval(
                Timestamp("2012-12-31 23:57:07.200000", tz=tz),
                Timestamp("2013-01-01 16:00:00", tz=tz),
            ),
            Interval(
                Timestamp("2013-01-01 16:00:00", tz=tz),
                Timestamp("2013-01-02 08:00:00", tz=tz),
            ),
            Interval(
                Timestamp("2013-01-02 08:00:00", tz=tz),
                Timestamp("2013-01-03 00:00:00", tz=tz),
            ),
        ]
    )
    if isinstance(bins, int):
        # the dtype is inferred from ser, which has nanosecond unit
        ii = ii.astype("interval[datetime64[ns, US/Eastern]]")
    expected = Series(ii).astype(CategoricalDtype(ordered=True))
    tm.assert_series_equal(result, expected)

