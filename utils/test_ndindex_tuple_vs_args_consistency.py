
def test_ndindex_tuple_vs_args_consistency():
    """Test that ndindex(shape) and ndindex(*shape) produce same results."""
    # Single dimension
    assert_equal(list(np.ndindex(5)), list(np.ndindex((5,))))

    # Multiple dimensions
    assert_equal(list(np.ndindex(2, 3)), list(np.ndindex((2, 3))))

    # Complex shape
    shape = (2, 1, 4)
    assert_equal(list(np.ndindex(*shape)), list(np.ndindex(shape)))

