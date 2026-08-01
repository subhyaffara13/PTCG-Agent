
def test_series_array_string_dtype(any_string_dtype):
    ser = Series(["a", "b"], dtype=any_string_dtype)
    arr = np.asarray(ser)
    if any_string_dtype == "string" and any_string_dtype.storage == "pyarrow":
        # for pyarrow strings, the numpy arrays is not a view, so also does
        # not need to be read-only (https://github.com/pandas-dev/pandas/pull/64035)
        assert not np.shares_memory(arr, get_array(ser))
        assert arr.flags.writeable is True
    else:
        assert np.shares_memory(arr, get_array(ser))
        assert arr.flags.writeable is False

