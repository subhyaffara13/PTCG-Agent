
def test_expanding_corr(series):
    A = series.dropna()
    B = (A + np.random.default_rng(2).standard_normal(len(A)))[:-5]

    result = A.expanding().corr(B)

    rolling_result = A.rolling(window=len(A), min_periods=1).corr(B)

    tm.assert_almost_equal(rolling_result, result)

