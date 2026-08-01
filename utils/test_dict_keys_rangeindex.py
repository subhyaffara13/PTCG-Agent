
def test_dict_keys_rangeindex():
    result = Series({0: 1, 1: 2})
    expected = Series([1, 2], index=RangeIndex(2))
    tm.assert_series_equal(result, expected, check_index_type=True)

