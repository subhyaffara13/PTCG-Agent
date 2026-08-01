
def test_constructor_with_data(any_numpy_array):
    nparr = any_numpy_array
    arr = NumpyExtensionArray(nparr)
    assert arr.dtype.numpy_dtype == nparr.dtype

