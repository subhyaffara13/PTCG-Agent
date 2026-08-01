
def test_nans_count():
    obj = Series(np.random.default_rng(2).standard_normal(50))
    obj[:10] = np.nan
    obj[-10:] = np.nan
    result = obj.rolling(50, min_periods=30).count()
    tm.assert_almost_equal(
        result.iloc[-1], np.isfinite(obj[10:-10]).astype(float).sum()
    )

