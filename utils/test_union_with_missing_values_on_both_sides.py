
def test_union_with_missing_values_on_both_sides(nulls_fixture):
    # GH#38623
    mi1 = MultiIndex.from_arrays([[1, nulls_fixture]])
    mi2 = MultiIndex.from_arrays([[1, nulls_fixture, 3]])
    result = mi1.union(mi2)
    expected = MultiIndex.from_arrays([[1, 3, nulls_fixture]])
    tm.assert_index_equal(result, expected)

