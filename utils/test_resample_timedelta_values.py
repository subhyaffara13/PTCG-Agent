
def test_resample_timedelta_values():
    # GH 13119
    # check that timedelta dtype is preserved when NaT values are
    # introduced by the resampling

    times = timedelta_range("1 day", "6 day", freq="4D")
    df = DataFrame({"time": times}, index=times)

    times2 = timedelta_range("1 day", "6 day", freq="2D")
    exp = Series(times2, index=times2, name="time")
    exp.iloc[1] = pd.NaT

    res = df.resample("2D").first()["time"]
    tm.assert_series_equal(res, exp)
    res = df["time"].resample("2D").first()
    tm.assert_series_equal(res, exp)

