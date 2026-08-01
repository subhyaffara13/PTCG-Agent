
def test_setitem_object_typecode(dtype):
    arr = NumpyExtensionArray(np.array(["a", "b", "c"], dtype=dtype))
    arr[0] = "t"
    expected = NumpyExtensionArray(np.array(["t", "b", "c"], dtype=dtype))
    tm.assert_extension_array_equal(arr, expected)

