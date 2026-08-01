
def test_array_copy():
    a = np.array([1, 2])
    # default is to copy
    b = pd.array(a, dtype=a.dtype)
    assert not tm.shares_memory(a, b)

    # copy=True
    b = pd.array(a, dtype=a.dtype, copy=True)
    assert not tm.shares_memory(a, b)

    # copy=False
    b = pd.array(a, dtype=a.dtype, copy=False)
    assert tm.shares_memory(a, b)

