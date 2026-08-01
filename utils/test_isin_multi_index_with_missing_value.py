
def test_isin_multi_index_with_missing_value(labels, expected, level):
    # GH 19132
    midx = MultiIndex.from_arrays([[np.nan, "a", "b"], ["c", "d", np.nan]])
    result = midx.isin(labels, level=level)
    expected = np.array(expected)
    tm.assert_numpy_array_equal(result, expected)

