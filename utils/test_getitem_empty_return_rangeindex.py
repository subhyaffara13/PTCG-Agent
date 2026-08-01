
def test_getitem_empty_return_rangeindex():
    result = RangeIndex(0, 10, 2, name="foo")[[]]
    expected = RangeIndex(start=0, stop=0, step=1, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

