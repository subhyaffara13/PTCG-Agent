
def test_resample_origin_with_day_freq_on_dst(unit):
    # GH 31809
    tz = "America/Chicago"
    msg = "The '(origin|offset)' keyword does not take effect"

    def _create_series(values, timestamps, freq="D"):
        return Series(
            values,
            index=DatetimeIndex(
                [Timestamp(t, tz=tz) for t in timestamps], freq=freq, ambiguous=True
            ).as_unit(unit),
        )

    # test classical behavior of origin in a DST context
    start = Timestamp("2013-11-02", tz=tz)
    end = Timestamp("2013-11-03 23:59", tz=tz)
    rng = date_range(start, end, freq="1h").as_unit(unit)
    ts = Series(np.ones(len(rng)), index=rng)

    expected = _create_series([24.0, 25.0], ["2013-11-02", "2013-11-03"])
    for origin in ["epoch", "start", "start_day", start, None]:
        warn = RuntimeWarning if origin != "start_day" else None
        with tm.assert_produces_warning(warn, match=msg):
            result = ts.resample("D", origin=origin).sum()
        tm.assert_series_equal(result, expected)

    # test complex behavior of origin/offset in a DST context
    start = Timestamp("2013-11-03", tz=tz)
    end = Timestamp("2013-11-03 23:59", tz=tz)
    rng = date_range(start, end, freq="1h").as_unit(unit)
    ts = Series(np.ones(len(rng)), index=rng)

    # GH#61985 changed this to behave like "B" rather than "24h"
    expected_ts = ["2013-11-03 00:00-05:00"]
    expected = _create_series([25.0], expected_ts)
    with tm.assert_produces_warning(RuntimeWarning, match=msg):
        result = ts.resample("D", origin="start", offset="-2h").sum()
    tm.assert_series_equal(result, expected)

    expected_ts = ["2013-11-02 22:00-05:00", "2013-11-03 21:00-06:00"]
    expected = _create_series([22.0, 3.0], expected_ts, freq="24h")
    result = ts.resample("24h", origin="start", offset="-2h").sum()
    tm.assert_series_equal(result, expected)

    # GH#61985 changed this to behave like "B" rather than "24h"
    expected_ts = ["2013-11-03 00:00-05:00"]
    expected = _create_series([25.0], expected_ts)
    with tm.assert_produces_warning(RuntimeWarning, match=msg):
        result = ts.resample("D", origin="start", offset="2h").sum()
    tm.assert_series_equal(result, expected)

    expected_ts = ["2013-11-03 00:00-05:00"]
    expected = _create_series([25.0], expected_ts)
    with tm.assert_produces_warning(RuntimeWarning, match=msg):
        result = ts.resample("D", origin="start", offset="-1h").sum()
    tm.assert_series_equal(result, expected)

    expected_ts = ["2013-11-03 00:00-05:00"]
    expected = _create_series([25.0], expected_ts)
    with tm.assert_produces_warning(RuntimeWarning, match=msg):
        result = ts.resample("D", origin="start", offset="1h").sum()
    tm.assert_series_equal(result, expected)

