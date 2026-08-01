
def test_cmov_window_special_linear_range(win_types_special, step):
    # GH 8238
    pytest.importorskip("scipy")
    kwds = {
        "kaiser": {"beta": 1.0},
        "gaussian": {"std": 1.0},
        "general_gaussian": {"p": 2.0, "sig": 2.0},
        "slepian": {"width": 0.5},
        "exponential": {"tau": 10},
    }

    vals = np.array(range(10), dtype=float)
    rs = (
        Series(vals)
        .rolling(5, win_type=win_types_special, center=True, step=step)
        .mean(**kwds[win_types_special])
    )
    xp = vals
    xp[:2] = np.nan
    xp[-2:] = np.nan
    xp = Series(xp)[::step]
    tm.assert_series_equal(xp, rs)

