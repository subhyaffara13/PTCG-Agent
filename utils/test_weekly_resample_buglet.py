
def test_weekly_resample_buglet(unit):
    # #1327
    rng = date_range("1/1/2000", freq="B", periods=20).as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)

    resampled = ts.resample("W").mean()
    expected = ts.resample("W-SUN").mean()
    tm.assert_series_equal(resampled, expected)

