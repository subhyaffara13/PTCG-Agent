
def test_void_arraylike_trumps_byteslike():
    # The memoryview is converted as an array-like of shape (18,)
    # rather than a single bytes-like of that length.
    m = memoryview(b"just one mintleaf?")
    res = np.void(m)
    assert type(res) is np.ndarray
    assert res.dtype == "V1"
    assert res.shape == (18,)

