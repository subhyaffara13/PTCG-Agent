
def test_getitem_generator(string_series):
    gen = (x > 0 for x in string_series)
    result = string_series[gen]
    result2 = string_series[iter(string_series > 0)]
    expected = string_series[string_series > 0]
    tm.assert_series_equal(result, expected)
    tm.assert_series_equal(result2, expected)

