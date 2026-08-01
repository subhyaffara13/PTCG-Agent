
def test_rolling_corr_with_zero_variance(window):
    # GH 18430
    s = Series(np.zeros(20))
    other = Series(np.arange(20))

    assert s.rolling(window=window).corr(other=other).isna().all()

