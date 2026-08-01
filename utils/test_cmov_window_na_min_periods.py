
def test_cmov_window_na_min_periods(step, min_periods):
    pytest.importorskip("scipy")
    vals = Series(np.random.default_rng(2).standard_normal(10))
    vals[4] = np.nan
    vals[8] = np.nan

    xp = vals.rolling(5, min_periods=min_periods, center=True, step=step).mean()
    rs = vals.rolling(
        5, win_type="boxcar", min_periods=min_periods, center=True, step=step
    ).mean()
    tm.assert_series_equal(xp, rs)

