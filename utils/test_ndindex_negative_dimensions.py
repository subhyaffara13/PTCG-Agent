
def test_ndindex_negative_dimensions(negative_shape_arg):
    """Test that negative dimensions raise ValueError."""
    with pytest.raises(ValueError):
        ndindex(negative_shape_arg)

