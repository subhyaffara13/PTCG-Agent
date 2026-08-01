
def test_shares_memory_api():
    x = np.zeros([4, 5, 6], dtype=np.int8)

    assert_equal(np.shares_memory(x, x), True)
    assert_equal(np.shares_memory(x, x.copy()), False)

    a = x[:, ::2, ::3]
    b = x[:, ::3, ::2]
    assert_equal(np.shares_memory(a, b), True)
    assert_equal(np.shares_memory(a, b, max_work=None), True)
    assert_raises(
        np.exceptions.TooHardError, np.shares_memory, a, b, max_work=1
    )

