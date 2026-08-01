
def test_sortlevel_not_sort_remaining():
    mi = MultiIndex.from_tuples([[1, 1, 3], [1, 1, 1]], names=list("ABC"))
    sorted_idx, _ = mi.sortlevel("A", sort_remaining=False)
    assert sorted_idx.equals(mi)

