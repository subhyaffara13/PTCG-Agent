
def test_multiindex_compare():
    # GH 21149
    # Ensure comparison operations for MultiIndex with nlevels == 1
    # behave consistently with those for MultiIndex with nlevels > 1

    midx = MultiIndex.from_product([[0, 1]])

    # Equality self-test: MultiIndex object vs self
    expected = Series([True, True])
    result = Series(midx == midx)
    tm.assert_series_equal(result, expected)

    # Greater than comparison: MultiIndex object vs self
    expected = Series([False, False])
    result = Series(midx > midx)
    tm.assert_series_equal(result, expected)

