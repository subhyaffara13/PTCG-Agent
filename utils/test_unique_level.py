
def test_unique_level(idx, level):
    # GH #17896 - with level= argument
    result = idx.unique(level=level)
    expected = idx.get_level_values(level).unique()
    tm.assert_index_equal(result, expected)

    # With already unique level
    mi = MultiIndex.from_arrays([[1, 3, 2, 4], [1, 3, 2, 5]], names=["first", "second"])
    result = mi.unique(level=level)
    expected = mi.get_level_values(level)
    tm.assert_index_equal(result, expected)

    # With empty MI
    mi = MultiIndex.from_arrays([[], []], names=["first", "second"])
    result = mi.unique(level=level)
    expected = mi.get_level_values(level)
    tm.assert_index_equal(result, expected)

