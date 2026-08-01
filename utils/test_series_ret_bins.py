
def test_series_ret_bins():
    # see gh-8589
    ser = Series(np.arange(4))
    result, bins = cut(ser, 2, retbins=True)

    expected = Series(
        IntervalIndex.from_breaks([-0.003, 1.5, 3], closed="right").repeat(2)
    ).astype(CategoricalDtype(ordered=True))
    tm.assert_series_equal(result, expected)

