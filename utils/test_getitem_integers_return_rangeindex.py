
def test_getitem_integers_return_rangeindex():
    result = RangeIndex(0, 10, 2, name="foo")[[0, -1]]
    expected = RangeIndex(start=0, stop=16, step=8, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

    result = RangeIndex(0, 10, 2, name="foo")[[3]]
    expected = RangeIndex(start=6, stop=8, step=2, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

