
def test_getitem_with_duplicates_indices(result_1, duplicate_item, expected_1):
    # GH 17610
    result_1 = Series(result_1)
    duplicate_item = Series(duplicate_item)
    result = result_1._append_internal(duplicate_item)
    expected = expected_1._append_internal(duplicate_item)
    tm.assert_series_equal(result[1], expected)
    assert result[2] == result_1[2]

