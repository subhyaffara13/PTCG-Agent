
def test_as_strided_checked_2d_default_strides(shape):
    """Test 2D arrays with default strides."""
    x = np.arange(np.prod(shape), dtype=np.int64).reshape(shape)
    y = as_strided(x, check_bounds=True)  # Should use default shape and strides
    assert_array_equal(y, x)

