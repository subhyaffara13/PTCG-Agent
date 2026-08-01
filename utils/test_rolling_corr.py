
def test_rolling_corr(series):
    A = series
    B = A + np.random.default_rng(2).standard_normal(len(A))

    result = A.rolling(window=50, min_periods=25).corr(B)
    tm.assert_almost_equal(result.iloc[-1], np.corrcoef(A[-50:], B[-50:])[0, 1])

