
def test_constructor_copy_input_ndarray_default():
    arr = np.array([0, 1])
    idx = Index(arr)
    assert not np.shares_memory(arr, get_array(idx))

