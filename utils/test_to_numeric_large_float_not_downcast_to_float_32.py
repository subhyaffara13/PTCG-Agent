
def test_to_numeric_large_float_not_downcast_to_float_32(val):
    # GH 19729
    expected = Series([val])
    result = to_numeric(expected, downcast="float")
    tm.assert_series_equal(result, expected)

