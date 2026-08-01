
def test_downsample_across_dst(unit):
    # GH 8531
    tz = zoneinfo.ZoneInfo("Europe/Berlin")
    dt = datetime(2014, 10, 26)
    dates = date_range(dt.astimezone(tz), periods=4, freq="2h").as_unit(unit)
    result = Series(5, index=dates).resample("h").mean()
    expected = Series(
        [5.0, np.nan] * 3 + [5.0],
        index=date_range(dt.astimezone(tz), periods=7, freq="h").as_unit(unit),
    )
    tm.assert_series_equal(result, expected)

