
def test_as_strided_checked_zero_stride_broadcasting(size):
    """Test zero strides (broadcasting a single value)."""
    x = np.array([42], dtype=np.int64)
    y = as_strided(x, shape=(size,), strides=(0,), check_bounds=True)
    assert y.shape == (size,)
    if size > 0:
        assert_(np.all(y == 42))

