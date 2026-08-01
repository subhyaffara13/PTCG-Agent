
def test_reduceat_empty():
    """Reduceat should work with empty arrays"""
    indices = np.array([], 'i4')
    x = np.array([], 'f8')
    result = np.add.reduceat(x, indices)
    assert_equal(result.dtype, x.dtype)
    assert_equal(result.shape, (0,))
    # Another case with a slightly different zero-sized shape
    x = np.ones((5, 2))
    result = np.add.reduceat(x, [], axis=0)
    assert_equal(result.dtype, x.dtype)
    assert_equal(result.shape, (0, 2))
    result = np.add.reduceat(x, [], axis=1)
    assert_equal(result.dtype, x.dtype)
    assert_equal(result.shape, (5, 0))

