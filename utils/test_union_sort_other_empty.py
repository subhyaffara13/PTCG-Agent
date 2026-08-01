
def test_union_sort_other_empty(slice_):
    # https://github.com/pandas-dev/pandas/issues/24959
    idx = MultiIndex.from_product([[1, 0], ["a", "b"]])

    # default, sort=None
    other = idx[slice_]
    tm.assert_index_equal(idx.union(other), idx)
    tm.assert_index_equal(other.union(idx), idx)

    # sort=False
    tm.assert_index_equal(idx.union(other, sort=False), idx)

