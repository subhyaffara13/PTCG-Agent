
def test_abs_returns_rangeindex(rng, exp_rng):
    ri = RangeIndex(rng, name="foo")
    expected = RangeIndex(exp_rng, name="foo")
    result = abs(ri)
    tm.assert_index_equal(result, expected, exact=True)

