
def test_insert_empty_0_loc():
    ri = RangeIndex(0, step=10, name="foo")
    result = ri.insert(0, 5)
    expected = RangeIndex(5, 15, 10, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

