
def test_tolist_scalar_dtype(values, dtype, expected_dtype):
    # GH49890
    ser = Series(values, dtype=dtype)
    result_dtype = type(ser.tolist()[0])
    assert result_dtype == expected_dtype

