
def test_union_empty_self_different_names():
    # GH#38423
    mi = MultiIndex.from_arrays([[]])
    mi2 = MultiIndex.from_arrays([[1, 2], [3, 4]], names=["a", "b"])
    result = mi.union(mi2)
    expected = MultiIndex.from_arrays([[1, 2], [3, 4]])
    tm.assert_index_equal(result, expected)

