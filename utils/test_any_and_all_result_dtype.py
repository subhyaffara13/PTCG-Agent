
def test_any_and_all_result_dtype(dtype):
    arr = np.ones(3, dtype=dtype)
    assert np.any(arr).dtype == np.bool
    assert np.all(arr).dtype == np.bool

