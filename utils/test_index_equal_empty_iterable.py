
def test_index_equal_empty_iterable():
    # #16844
    a = MultiIndex(levels=[[], []], codes=[[], []], names=["a", "b"])
    b = MultiIndex.from_arrays(arrays=[[], []], names=["a", "b"])
    tm.assert_index_equal(a, b)

