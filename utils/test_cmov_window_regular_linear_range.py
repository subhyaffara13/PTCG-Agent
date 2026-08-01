
def test_cmov_window_regular_linear_range(win_types, step):
    # GH 8238
    pytest.importorskip("scipy")
    vals = np.array(range(10), dtype=float)
    rs = Series(vals).rolling(5, win_type=win_types, center=True, step=step).mean()
    xp = vals
    xp[:2] = np.nan
    xp[-2:] = np.nan
    xp = Series(xp)[::step]

    tm.assert_series_equal(xp, rs)

