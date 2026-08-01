
def test_as_strided_checked_out_of_bounds_positive_strides(size, shape, strides):
    """Test that out-of-bounds positive strides raise ValueError."""
    x = np.arange(size, dtype=np.int64)
    with pytest.raises(ValueError, match="out of bounds"):
        as_strided(x, shape=shape, strides=strides, check_bounds=True)

