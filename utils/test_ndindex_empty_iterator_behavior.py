
def test_ndindex_empty_iterator_behavior():
    """Test detailed behavior of empty iterators."""
    empty_iter = np.ndindex(0, 5)
    assert_equal(list(empty_iter), [])

    empty_iter2 = np.ndindex(3, 0, 2)
    with pytest.raises(StopIteration):
        next(empty_iter2)

