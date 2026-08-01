
def test_upsample_with_limit(unit):
    rng = date_range("1/1/2000", periods=3, freq="5min").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), rng)

    result = ts.resample("min").ffill(limit=2)
    expected = ts.reindex(result.index, method="ffill", limit=2)
    tm.assert_series_equal(result, expected)

