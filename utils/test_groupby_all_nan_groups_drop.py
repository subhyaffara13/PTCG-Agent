
def test_groupby_all_nan_groups_drop():
    # GH 15036
    s = Series([1, 2, 3], [np.nan, np.nan, np.nan])
    result = s.groupby(s.index).sum()
    expected = Series([], index=Index([], dtype=np.float64), dtype=np.int64)
    tm.assert_series_equal(result, expected)

