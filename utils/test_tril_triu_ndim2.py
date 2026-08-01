
def test_tril_triu_ndim2():
    for dtype in np.typecodes['AllFloat'] + np.typecodes['AllInteger']:
        a = np.ones((2, 2), dtype=dtype)
        b = np.tril(a)
        c = np.triu(a)
        assert_array_equal(b, [[1, 0], [1, 1]])
        assert_array_equal(c, b.T)
        # should return the same dtype as the original array
        assert_equal(b.dtype, a.dtype)
        assert_equal(c.dtype, a.dtype)

