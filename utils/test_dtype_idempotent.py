
def test_dtype_idempotent(any_numpy_dtype):
    dtype = NumpyEADtype(any_numpy_dtype)

    result = NumpyEADtype(dtype)
    assert result == dtype

