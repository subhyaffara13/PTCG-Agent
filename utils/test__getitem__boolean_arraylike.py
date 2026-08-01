
def test__getitem__boolean_arraylike(container):
    ri = RangeIndex(5)
    result = ri[container([True, True, False, False, True])]
    expected = Index([0, 1, 4], dtype="int64")
    tm.assert_index_equal(result, expected)

