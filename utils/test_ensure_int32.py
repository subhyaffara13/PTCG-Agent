
def test_ensure_int32():
    values = np.arange(10, dtype=np.int32)
    result = ensure_int32(values)
    assert result.dtype == np.int32

    values = np.arange(10, dtype=np.int64)
    result = ensure_int32(values)
    assert result.dtype == np.int32

