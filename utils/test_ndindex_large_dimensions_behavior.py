
def test_ndindex_large_dimensions_behavior():
    """Test ndindex behaves correctly when initialized with large dimensions."""
    large_shape = (1000, 1000)
    iter_obj = np.ndindex(*large_shape)
    first_element = next(iter_obj)
    assert_equal(first_element, (0, 0))

