
def test_getitem_setitem_datetime_tz(tz_source):
    if tz_source == "pytz":
        pytz = pytest.importorskip(tz_source)
        tzget = pytz.timezone
    else:
        # handle special case for utc in dateutil
        tzget = lambda x: tzutc() if x == "UTC" else gettz(x)

    N = 50
    # testing with timezone, GH #2785
    rng = date_range("1/1/1990", periods=N, freq="h", tz=tzget("US/Eastern"))
    ts = Series(np.random.default_rng(2).standard_normal(N), index=rng)

    # also test Timestamp tz handling, GH #2789
    result = ts.copy()
    result["1990-01-01 09:00:00+00:00"] = 0
    result["1990-01-01 09:00:00+00:00"] = ts.iloc[4]
    tm.assert_series_equal(result, ts)

    result = ts.copy()
    result["1990-01-01 03:00:00-06:00"] = 0
    result["1990-01-01 03:00:00-06:00"] = ts.iloc[4]
    tm.assert_series_equal(result, ts)

    # repeat with datetimes
    result = ts.copy()
    result[datetime(1990, 1, 1, 9, tzinfo=tzget("UTC"))] = 0
    result[datetime(1990, 1, 1, 9, tzinfo=tzget("UTC"))] = ts.iloc[4]
    tm.assert_series_equal(result, ts)

    result = ts.copy()
    dt = Timestamp(1990, 1, 1, 3).tz_localize(tzget("US/Central"))
    dt = dt.to_pydatetime()
    result[dt] = 0
    result[dt] = ts.iloc[4]
    tm.assert_series_equal(result, ts)

