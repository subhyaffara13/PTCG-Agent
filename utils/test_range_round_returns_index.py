
def test_range_round_returns_index(rng, decimals):
    ri = RangeIndex(rng)
    expected = Index(list(rng)).round(decimals=decimals)
    result = ri.round(decimals=decimals)
    tm.assert_index_equal(result, expected, exact=True)

