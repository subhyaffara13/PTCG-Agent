
def test_ohlc_5min(unit):
    def _ohlc(group):
        if isna(group).all():
            return np.repeat(np.nan, 4)
        return [group.iloc[0], group.max(), group.min(), group.iloc[-1]]

    rng = date_range("1/1/2000 00:00:00", "1/1/2000 5:59:50", freq="10s").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)

    resampled = ts.resample("5min", closed="right", label="right").ohlc()

    assert (resampled.loc["1/1/2000 00:00"] == ts.iloc[0]).all()

    exp = _ohlc(ts[1:31])
    assert (resampled.loc["1/1/2000 00:05"] == exp).all()

    exp = _ohlc(ts["1/1/2000 5:55:01":])
    assert (resampled.loc["1/1/2000 6:00:00"] == exp).all()

