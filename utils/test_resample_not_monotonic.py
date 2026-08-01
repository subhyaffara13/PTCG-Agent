
def test_resample_not_monotonic(unit):
    rng = date_range("2012-06-12", periods=200, freq="h").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)

    ts = ts.take(np.random.default_rng(2).permutation(len(ts)))

    result = ts.resample("D").sum()
    exp = ts.sort_index().resample("D").sum()
    tm.assert_series_equal(result, exp)

