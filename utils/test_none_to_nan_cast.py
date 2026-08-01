
def test_none_to_nan_cast(dtype):
    # Note that at the time of writing this test, the scalar constructors
    # reject None
    arr = np.zeros(1, dtype=dtype)
    arr[0] = None
    assert np.isnan(arr)[0]
    assert np.isnan(np.array(None, dtype=dtype))[()]
    assert np.isnan(np.array([None], dtype=dtype))[0]
    assert np.isnan(np.array(None).astype(dtype))[()]

