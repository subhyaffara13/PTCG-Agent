
def test_sortlevel_na_position():
    # GH#51612
    midx = MultiIndex.from_tuples([(1, np.nan), (1, 1)])
    result = midx.sortlevel(level=[0, 1], na_position="last")[0]
    expected = MultiIndex.from_tuples([(1, 1), (1, np.nan)])
    tm.assert_index_equal(result, expected)

