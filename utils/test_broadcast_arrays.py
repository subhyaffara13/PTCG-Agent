
def test_broadcast_arrays():
    # Test user defined dtypes
    dtype = 'u4,u4,u4'
    a = np.array([(1, 2, 3)], dtype=dtype)
    b = np.array([(1, 2, 3), (4, 5, 6), (7, 8, 9)], dtype=dtype)
    result = np.broadcast_arrays(a, b)
    assert_equal(result[0], np.array([(1, 2, 3), (1, 2, 3), (1, 2, 3)], dtype=dtype))
    assert_equal(result[1], np.array([(1, 2, 3), (4, 5, 6), (7, 8, 9)], dtype=dtype))

