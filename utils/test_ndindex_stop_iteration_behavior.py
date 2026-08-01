
def test_ndindex_stop_iteration_behavior():
    """Test that StopIteration is raised properly after exhaustion."""
    it = np.ndindex(2, 2)
    # Exhaust the iterator
    list(it)
    # Should raise StopIteration on subsequent calls
    with pytest.raises(StopIteration):
        next(it)

