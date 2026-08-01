
def test_as_strided_checked_sliced_array():
    """Test various slicing scenarios."""
    a = np.arange(200, dtype=np.int64)

    b = a[10:20]
    y = as_strided(b, shape=(5,), strides=(16,), check_bounds=True)
    assert_equal(y.shape, (5,))

    c = a[::2]
    y = as_strided(c, shape=(10,), strides=(16,), check_bounds=True)
    assert_equal(y.shape, (10,))

