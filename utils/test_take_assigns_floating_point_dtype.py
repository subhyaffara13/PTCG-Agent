
def test_take_assigns_floating_point_dtype(dtype):
    # GH#62448.
    if dtype == np.bool_:
        array = NumpyExtensionArray(np.array([False, True, False], dtype=dtype))
        expected = np.dtype(object)
    else:
        array = NumpyExtensionArray(np.array([1, 2, 3], dtype=dtype))
        expected = np.float64

    result = array.take([-1], allow_fill=True)
    assert result.dtype.numpy_dtype == expected

    result = array.take([-1], allow_fill=True, fill_value=5.0)
    assert result.dtype.numpy_dtype == expected

