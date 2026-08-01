
def test_basic_binop():
    # Just a basic smoke test. The EA interface tests exercise this
    # more thoroughly.
    x = NumpyExtensionArray(np.array([1, 2, 3]))
    result = x + x
    expected = NumpyExtensionArray(np.array([2, 4, 6]))
    tm.assert_extension_array_equal(result, expected)

