
def test_isin_filtering_on_iterable(data, isin):
    # GH 50234

    ser = Series(data)
    result = ser.isin(i for i in isin)
    expected_result = Series([True, True, False])

    tm.assert_series_equal(result, expected_result)

