
def test_intersection_equal_different_names():
    # GH#30302
    mi1 = MultiIndex.from_arrays([[1, 2], [3, 4]], names=["c", "b"])
    mi2 = MultiIndex.from_arrays([[1, 2], [3, 4]], names=["a", "b"])

    result = mi1.intersection(mi2)
    expected = MultiIndex.from_arrays([[1, 2], [3, 4]], names=[None, "b"])
    tm.assert_index_equal(result, expected)

