
def test_shares_memory_numpy():
    arr = np.arange(10)
    view = arr[:5]
    assert tm.shares_memory(arr, view)
    arr2 = np.arange(10)
    assert not tm.shares_memory(arr, arr2)

