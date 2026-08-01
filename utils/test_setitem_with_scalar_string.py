
def test_setitem_with_scalar_string(dtype):
    # is_float_dtype considers some strings, like 'd', to be floats
    # which can cause issues.
    arr = pd.array(["a", "c"], dtype=dtype)
    arr[0] = "d"
    expected = pd.array(["d", "c"], dtype=dtype)
    tm.assert_extension_array_equal(arr, expected)

