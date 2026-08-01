
def test_ndindex_non_integer_dimensions(bad_shape):
    """Test that non-integer dimensions raise TypeError."""
    with pytest.raises(TypeError):
        # Passing invalid_shape_arg directly to ndindex. It will try to use it
        # as a dimension and should trigger a TypeError.
        list(np.ndindex(bad_shape))

