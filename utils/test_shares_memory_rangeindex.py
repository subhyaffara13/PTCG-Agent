
def test_shares_memory_rangeindex():
    idx = pd.RangeIndex(10)
    arr = np.arange(10)
    assert not tm.shares_memory(idx, arr)

