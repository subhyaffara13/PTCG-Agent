
def test_may_share_memory_bad_max_work():
    x = np.zeros([1])
    assert_raises(OverflowError, np.may_share_memory, x, x, max_work=10**100)
    assert_raises(OverflowError, np.shares_memory, x, x, max_work=10**100)

