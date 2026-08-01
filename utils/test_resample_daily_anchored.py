
def test_resample_daily_anchored(unit):
    rng = date_range("1/1/2000 0:00:00", periods=10000, freq="min").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)
    ts[:2] = np.nan  # so results are the same

    result = ts[2:].resample("D", closed="left", label="left").mean()
    expected = ts.resample("D", closed="left", label="left").mean()
    tm.assert_series_equal(result, expected)

