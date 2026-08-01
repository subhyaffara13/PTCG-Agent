
def test_numpy_array_all_dtypes(any_numpy_dtype):
    ser = Series(dtype=any_numpy_dtype)
    result = ser.array
    if np.dtype(any_numpy_dtype).kind == "M":
        assert isinstance(result, DatetimeArray)
    elif np.dtype(any_numpy_dtype).kind == "m":
        assert isinstance(result, TimedeltaArray)
    else:
        assert isinstance(result, NumpyExtensionArray)

