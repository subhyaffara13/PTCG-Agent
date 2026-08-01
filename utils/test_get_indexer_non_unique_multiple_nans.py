
def test_get_indexer_non_unique_multiple_nans(idx, target, expected):
    # GH 35392
    axis = Index(idx)
    actual = axis.get_indexer_for(target)
    tm.assert_numpy_array_equal(actual, expected)

