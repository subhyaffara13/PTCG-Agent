
def test_bandwidth_square_inputs(T):
    n = 20
    k = 4
    R = np.zeros([n, n], dtype=T, order='F')
    # form a banded matrix inplace
    R[[x for x in range(n)], [x for x in range(n)]] = 1
    R[[x for x in range(n-k)], [x for x in range(k, n)]] = 1
    R[[x for x in range(1, n)], [x for x in range(n-1)]] = 1
    R[[x for x in range(k, n)], [x for x in range(n-k)]] = 1
    assert bandwidth(R) == (k, k)
    A = np.array([
        [1, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
    ])
    assert bandwidth(A) == (2, 2)

    A = np.array(
        [
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],  # diagonal
            [[0, 0, 1], [0, 0, 0], [0, 0, 0]],  # upper triangular
            [[0, 0, 0], [0, 0, 0], [1, 0, 0]],  # lower triangular
            [[0, 0, 1], [0, 0, 0], [1, 0, 0]],  # full
            [[0, 0, 1], [0, 0, 0], [0, 1, 0.]],  # upper hessenberg
        ]
    )
    lo, hi = bandwidth(A)
    assert_equal(lo, [0, 0, 2, 2, 1])
    assert_equal(hi, [0, 2, 0, 2, 2])

