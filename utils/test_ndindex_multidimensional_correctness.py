
def test_ndindex_multidimensional_correctness():
    """Test ndindex produces correct indices for multidimensional arrays."""
    shape = (2, 1, 3)
    result = list(np.ndindex(*shape))
    expected = [
        (0, 0, 0),
        (0, 0, 1),
        (0, 0, 2),
        (1, 0, 0),
        (1, 0, 1),
        (1, 0, 2),
    ]
    assert_equal(result, expected)

