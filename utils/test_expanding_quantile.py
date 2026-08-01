
def test_expanding_quantile(series):
    result = series.expanding().quantile(0.5)

    rolling_result = series.rolling(window=len(series), min_periods=1).quantile(0.5)

    tm.assert_almost_equal(result, rolling_result)

