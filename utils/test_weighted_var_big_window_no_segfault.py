
def test_weighted_var_big_window_no_segfault(win_types, center):
    # GitHub Issue #46772
    pytest.importorskip("scipy")
    x = Series(0)
    result = x.rolling(window=16, center=center, win_type=win_types).var()
    expected = Series(np.nan)

    tm.assert_series_equal(result, expected)

