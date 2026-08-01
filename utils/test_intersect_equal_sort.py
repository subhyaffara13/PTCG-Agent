
def test_intersect_equal_sort():
    # GH-24959
    idx = MultiIndex.from_product([[1, 0], ["a", "b"]])
    tm.assert_index_equal(idx.intersection(idx, sort=False), idx)
    tm.assert_index_equal(idx.intersection(idx, sort=None), idx)

