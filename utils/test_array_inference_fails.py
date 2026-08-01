
def test_array_inference_fails(data):
    result = pd.array(data)
    expected = NumpyExtensionArray(np.array(data, dtype=object))
    tm.assert_extension_array_equal(result, expected)

