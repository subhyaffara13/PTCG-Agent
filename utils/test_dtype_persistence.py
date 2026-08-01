
def test_dtype_persistence(dtype, mode):
    arr = np.zeros((3, 2, 1), dtype=dtype)
    result = np.pad(arr, 1, mode=mode)
    assert result.dtype == dtype

