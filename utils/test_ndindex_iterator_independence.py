
def test_ndindex_iterator_independence():
    """Test that each ndindex instance creates independent iterators."""
    shape = (2, 3)
    iter1 = np.ndindex(*shape)
    iter2 = np.ndindex(*shape)

    next(iter1)
    next(iter1)

    assert_equal(next(iter2), (0, 0))
    assert_equal(next(iter1), (0, 2))

