
def test_bins_monotonic_not_overflowing(x, bins, expected):
    # GH 26045
    result = cut(x, bins)
    tm.assert_index_equal(result.categories, expected)

