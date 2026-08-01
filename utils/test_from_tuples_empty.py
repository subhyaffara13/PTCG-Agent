
def test_from_tuples_empty():
    # GH 16777
    result = MultiIndex.from_tuples([], names=["a", "b"])
    expected = MultiIndex.from_arrays(arrays=[[], []], names=["a", "b"])
    tm.assert_index_equal(result, expected)

