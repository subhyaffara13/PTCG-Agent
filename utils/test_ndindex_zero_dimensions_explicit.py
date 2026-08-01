
def test_ndindex_zero_dimensions_explicit():
    """Test ndindex produces empty iterators for explicit
    zero-length dimensions."""
    assert list(np.ndindex(0, 3)) == []
    assert list(np.ndindex(3, 0, 2)) == []
    assert list(np.ndindex(0)) == []

