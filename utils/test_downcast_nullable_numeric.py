
def test_downcast_nullable_numeric(data, input_dtype, downcast, expected_dtype):
    arr = pd.array(data, dtype=input_dtype)
    result = to_numeric(arr, downcast=downcast)
    expected = pd.array(data, dtype=expected_dtype)
    tm.assert_extension_array_equal(result, expected)

