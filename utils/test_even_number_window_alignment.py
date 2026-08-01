
def test_even_number_window_alignment():
    # see discussion in GH 38780
    s = Series(range(3), index=date_range(start="2020-01-01", freq="D", periods=3))

    # behavior of index- and datetime-based windows differs here!
    # s.rolling(window=2, min_periods=1, center=True).mean()

    result = s.rolling(window="2D", min_periods=1, center=True).mean()

    expected = Series([0.5, 1.5, 2], index=s.index)

    tm.assert_series_equal(result, expected)

