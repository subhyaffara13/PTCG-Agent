
def test_ufunc_unary(ufunc):
    arr = NumpyExtensionArray(np.array([-1.0, 0.0, 1.0]))
    result = ufunc(arr)
    expected = NumpyExtensionArray(ufunc(arr._ndarray))
    tm.assert_extension_array_equal(result, expected)

    # same thing but with the 'out' keyword
    out = NumpyExtensionArray(np.array([-9.0, -9.0, -9.0]))
    ufunc(arr, out=out)
    tm.assert_extension_array_equal(out, expected)

