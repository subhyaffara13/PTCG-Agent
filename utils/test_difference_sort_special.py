
def test_difference_sort_special():
    # GH-24959
    idx = MultiIndex.from_product([[1, 0], ["a", "b"]])
    # sort=None, the default
    result = idx.difference([])
    tm.assert_index_equal(result, idx)

