
def test_cmov_window_corner(step):
    # GH 8238
    # all nan
    pytest.importorskip("scipy")
    vals = Series([np.nan] * 10)
    result = vals.rolling(5, center=True, win_type="boxcar", step=step).mean()
    assert np.isnan(result).all()

    # empty
    vals = Series([], dtype=object)
    result = vals.rolling(5, center=True, win_type="boxcar", step=step).mean()
    assert len(result) == 0

    # shorter than window
    vals = Series(np.random.default_rng(2).standard_normal(5))
    result = vals.rolling(10, win_type="boxcar", step=step).mean()
    assert np.isnan(result).all()
    assert len(result) == len(range(0, 5, step or 1))

