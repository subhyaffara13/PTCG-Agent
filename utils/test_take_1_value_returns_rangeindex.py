
def test_take_1_value_returns_rangeindex(rng, exp_rng):
    ri = RangeIndex(rng, name="foo")
    result = ri.take([3])
    expected = RangeIndex(exp_rng, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

