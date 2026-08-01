
def test_invert_returns_rangeindex(rng):
    ri = RangeIndex(rng, name="foo")
    result = ~ri
    assert isinstance(result, RangeIndex)
    expected = ~Index(list(rng), name="foo")
    tm.assert_index_equal(result, expected, exact=False)

