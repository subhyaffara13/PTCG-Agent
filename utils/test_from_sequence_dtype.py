
def test_from_sequence_dtype():
    arr = np.array([1, 2, 3], dtype="int64")
    result = NumpyExtensionArray._from_sequence(arr, dtype="uint64")
    expected = NumpyExtensionArray(np.array([1, 2, 3], dtype="uint64"))
    tm.assert_extension_array_equal(result, expected)

