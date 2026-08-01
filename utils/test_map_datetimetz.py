
def test_map_datetimetz():
    values = date_range("2011-01-01", "2011-01-02", freq="h").tz_localize("Asia/Tokyo")
    s = Series(values, name="XX")

    # keep tz
    result = s.map(lambda x: x + pd.offsets.Day())
    exp_values = date_range("2011-01-02", "2011-01-03", freq="h").tz_localize(
        "Asia/Tokyo"
    )
    exp = Series(exp_values, name="XX")
    tm.assert_series_equal(result, exp)

    result = s.map(lambda x: x.hour)
    exp = Series([*list(range(24)), 0], name="XX", dtype=np.int64)
    tm.assert_series_equal(result, exp)

    # not vectorized
    def f(x):
        if not isinstance(x, pd.Timestamp):
            raise ValueError
        return str(x.tz)

    result = s.map(f)
    exp = Series(["Asia/Tokyo"] * 25, name="XX")
    tm.assert_series_equal(result, exp)

