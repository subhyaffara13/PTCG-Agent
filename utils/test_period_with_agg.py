
def test_period_with_agg():
    # aggregate a period resampler with a lambda
    s2 = Series(
        np.random.default_rng(2).integers(0, 5, 50),
        index=period_range("2012-01-01", freq="h", periods=50),
        dtype="float64",
    )

    expected = s2.to_timestamp().resample("D").mean().to_period()
    result = s2.resample("D").agg(lambda x: x.mean())
    tm.assert_series_equal(result, expected)

