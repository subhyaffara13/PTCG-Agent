
def test_intersection_different_names():
    # GH#38323
    mi = MultiIndex.from_arrays([[1], [3]], names=["c", "b"])
    mi2 = MultiIndex.from_arrays([[1], [3]])
    result = mi.intersection(mi2)
    tm.assert_index_equal(result, mi2)

