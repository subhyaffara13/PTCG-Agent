
def test_take_preserves_boolean_arrays():
    array = NumpyExtensionArray(np.array([False, True, False], dtype=np.bool_))
    result = array.take([-1], allow_fill=False)
    assert result.dtype.numpy_dtype == np.bool_

