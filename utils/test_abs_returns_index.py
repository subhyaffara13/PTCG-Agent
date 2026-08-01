
def test_abs_returns_index():
    ri = RangeIndex(-2, 2, name="foo")
    result = abs(ri)
    expected = Index([2, 1, 0, 1], name="foo")
    tm.assert_index_equal(result, expected, exact=True)

