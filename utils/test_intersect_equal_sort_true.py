
def test_intersect_equal_sort_true():
    idx = MultiIndex.from_product([[1, 0], ["a", "b"]])
    expected = MultiIndex.from_product([[0, 1], ["a", "b"]])
    result = idx.intersection(idx, sort=True)
    tm.assert_index_equal(result, expected)

