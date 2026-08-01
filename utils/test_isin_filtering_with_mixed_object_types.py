
def test_isin_filtering_with_mixed_object_types(data, is_in):
    # GH 20883

    ser = Series(data)
    result = ser.isin(is_in)
    expected = Series([True, False])

    tm.assert_series_equal(result, expected)

