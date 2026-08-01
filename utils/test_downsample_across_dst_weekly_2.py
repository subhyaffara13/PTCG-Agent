
def test_downsample_across_dst_weekly_2(unit):
    # GH 9119, GH 21459
    idx = date_range("2013-04-01", "2013-05-01", tz="Europe/London", freq="h").as_unit(
        unit
    )
    s = Series(index=idx, dtype=np.float64)
    result = s.resample("W").mean()
    expected = Series(
        index=date_range("2013-04-07", freq="W", periods=5, tz="Europe/London").as_unit(
            unit
        ),
        dtype=np.float64,
    )
    tm.assert_series_equal(result, expected)

