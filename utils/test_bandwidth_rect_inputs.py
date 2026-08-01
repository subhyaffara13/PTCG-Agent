
def test_bandwidth_rect_inputs(T):
    n, m = 10, 20
    k = 5
    R = np.zeros([n, m], dtype=T, order='F')
    # form a banded matrix inplace
    R[[x for x in range(n)], [x for x in range(n)]] = 1
    R[[x for x in range(n-k)], [x for x in range(k, n)]] = 1
    R[[x for x in range(1, n)], [x for x in range(n-1)]] = 1
    R[[x for x in range(k, n)], [x for x in range(n-k)]] = 1
    assert bandwidth(R) == (k, k)

    R2 = np.tril(np.ones((2, 10, 2), dtype=T))
    lo, hi = bandwidth(R2)
    assert_equal(lo, [9, 9])
    assert_equal(hi, [0, 0])

    R3 = np.triu(np.ones((2, 10, 2), dtype=T))
    lo, hi = bandwidth(R3)
    assert_equal(lo, [0, 0])
    assert_equal(hi, [1, 1])

