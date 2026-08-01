
def test_range_round_returns_rangeindex(rng, decimals):
    ri = RangeIndex(rng)
    expected = ri.copy()
    result = ri.round(decimals=decimals)
    tm.assert_index_equal(result, expected, exact=True)

