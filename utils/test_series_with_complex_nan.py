
def test_series_with_complex_nan(input_list):
    # GH#53627
    ser = Series(input_list)
    result = Series(ser.array)
    assert ser.dtype == "complex128"
    tm.assert_series_equal(ser, result)

