
def test_iter_slice():
    a, b, c = np.arange(3), np.arange(3), np.arange(3.)
    i = nditer([a, b, c], [], ['readwrite'])
    with i:
        i[0:2] = (3, 3)
        assert_equal(a, [3, 1, 2])
        assert_equal(b, [3, 1, 2])
        assert_equal(c, [0, 1, 2])
        i[1] = 12
        assert_equal(i[0:2], [3, 12])

