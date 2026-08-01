
def test_intersection_with_missing_values_on_both_sides(nulls_fixture):
    # GH#38623
    mi1 = MultiIndex.from_arrays([[3, nulls_fixture, 4, nulls_fixture], [1, 2, 4, 2]])
    mi2 = MultiIndex.from_arrays([[3, nulls_fixture, 3], [1, 2, 4]])
    result = mi1.intersection(mi2)
    expected = MultiIndex.from_arrays([[3, nulls_fixture], [1, 2]])
    tm.assert_index_equal(result, expected)

