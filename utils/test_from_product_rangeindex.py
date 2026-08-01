
def test_from_product_rangeindex():
    # RangeIndex is preserved by factorize, so preserved in levels
    rng = Index(range(5))
    other = ["a", "b"]
    mi = MultiIndex.from_product([rng, other])
    tm.assert_index_equal(mi._levels[0], rng, exact=True)

