
def test_asarray_readonly(dtype):
    arr = pd.array([0.1, 0.2, 0.3], dtype="Float64")
    arr._readonly = True

    result = np.asarray(arr, dtype=dtype)
    assert not result.flags.writeable

    result = np.asarray(arr, dtype=dtype, copy=True)
    assert result.flags.writeable

    result = np.asarray(arr, dtype=dtype, copy=False)
    assert not result.flags.writeable


def test_asarray_readonly(dtype):
    arr = NumpyExtensionArray(np.array([1, 2, 3], dtype="int64"))
    arr._readonly = True
    result = np.asarray(arr, dtype=dtype)
    assert not result.flags.writeable

    result = np.asarray(arr, dtype=dtype, copy=True)
    assert result.flags.writeable

    result = np.asarray(arr, dtype=dtype, copy=False)
    assert not result.flags.writeable

