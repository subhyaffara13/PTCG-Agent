
def test_resample_anchored_ticks(freq, unit):
    # If a fixed delta (5 minute, 4 hour) evenly divides a day, we should
    # "anchor" the origin at midnight so we get regular intervals rather
    # than starting from the first timestamp which might start in the
    # middle of a desired interval

    rng = date_range("1/1/2000 04:00:00", periods=86400, freq="s").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)
    ts[:2] = np.nan  # so results are the same
    result = ts[2:].resample(freq, closed="left", label="left").mean()
    expected = ts.resample(freq, closed="left", label="left").mean()
    tm.assert_series_equal(result, expected)

