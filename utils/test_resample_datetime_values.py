
def test_resample_datetime_values(unit):
    # GH 13119
    # check that datetime dtype is preserved when NaT values are
    # introduced by the resampling

    dates = [datetime(2016, 1, 15), datetime(2016, 1, 19)]
    df = DataFrame({"timestamp": dates}, index=dates)
    df.index = df.index.as_unit(unit)

    exp = Series(
        [datetime(2016, 1, 15), pd.NaT, datetime(2016, 1, 19)],
        index=date_range("2016-01-15", periods=3, freq="2D").as_unit(unit),
        name="timestamp",
    )

    res = df.resample("2D").first()["timestamp"]
    tm.assert_series_equal(res, exp)
    res = df["timestamp"].resample("2D").first()
    tm.assert_series_equal(res, exp)

