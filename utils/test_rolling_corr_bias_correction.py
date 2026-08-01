
def test_rolling_corr_bias_correction():
    # test for correct bias correction
    a = Series(
        np.arange(20, dtype=np.float64), index=date_range("2020-01-01", periods=20)
    )
    b = a.copy()
    a[:5] = np.nan
    b[:10] = np.nan

    result = a.rolling(window=len(a), min_periods=1).corr(b)
    tm.assert_almost_equal(result.iloc[-1], a.corr(b))

