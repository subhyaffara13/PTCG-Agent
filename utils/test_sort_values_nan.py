
def test_sort_values_nan():
    # GH48495, GH48626
    midx = MultiIndex(levels=[["A", "B", "C"], ["D"]], codes=[[1, 0, 2], [-1, -1, 0]])
    result = midx.sort_values()
    expected = MultiIndex(
        levels=[["A", "B", "C"], ["D"]], codes=[[0, 1, 2], [-1, -1, 0]]
    )
    tm.assert_index_equal(result, expected)

