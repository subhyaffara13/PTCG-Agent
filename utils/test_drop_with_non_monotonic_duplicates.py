
def test_drop_with_non_monotonic_duplicates():
    # GH#33494
    mi = MultiIndex.from_tuples([(1, 2), (2, 3), (1, 2)])
    result = mi.drop((1, 2))
    expected = MultiIndex.from_tuples([(2, 3)])
    tm.assert_index_equal(result, expected)

