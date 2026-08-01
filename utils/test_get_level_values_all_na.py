
def test_get_level_values_all_na():
    # GH#17924 when level entirely consists of nan
    arrays = [[np.nan, np.nan, np.nan], ["a", np.nan, 1]]
    index = MultiIndex.from_arrays(arrays)
    result = index.get_level_values(0)
    expected = Index([np.nan, np.nan, np.nan], dtype=np.float64)
    tm.assert_index_equal(result, expected)

    result = index.get_level_values(1)
    expected = Index(["a", np.nan, 1], dtype=object)
    tm.assert_index_equal(result, expected)

