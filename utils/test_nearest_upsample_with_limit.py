
def test_nearest_upsample_with_limit(tz_aware_fixture, freq, rule, unit):
    # GH 33939
    rng = date_range("1/1/2000", periods=3, freq=freq, tz=tz_aware_fixture).as_unit(
        unit
    )
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), rng)

    result = ts.resample(rule).nearest(limit=2)
    expected = ts.reindex(result.index, method="nearest", limit=2)
    tm.assert_series_equal(result, expected)

