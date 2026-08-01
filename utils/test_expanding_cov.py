
def test_expanding_cov(series):
    A = series
    B = (A + np.random.default_rng(2).standard_normal(len(A)))[:-5]

    result = A.expanding().cov(B)

    rolling_result = A.rolling(window=len(A), min_periods=1).cov(B)

    tm.assert_almost_equal(rolling_result, result)

