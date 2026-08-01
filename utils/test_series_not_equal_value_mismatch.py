
def test_series_not_equal_value_mismatch(data1, data2):
    _assert_not_series_equal_both(Series(data1), Series(data2))

