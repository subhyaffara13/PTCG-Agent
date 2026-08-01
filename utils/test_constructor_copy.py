
def test_constructor_copy():
    arr = np.array([0, 1])
    result = NumpyExtensionArray(arr, copy=True)

    assert not tm.shares_memory(result, arr)

