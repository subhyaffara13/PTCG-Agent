
def test_getitem_integers_return_index():
    result = RangeIndex(0, 10, 2, name="foo")[[0, 1, -1]]
    expected = Index([0, 2, 8], dtype="int64", name="foo")
    tm.assert_index_equal(result, expected)

