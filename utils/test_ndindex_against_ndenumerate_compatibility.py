
def test_ndindex_against_ndenumerate_compatibility():
    """Test ndindex produces same indices as ndenumerate."""
    for shape in [(1, 2, 3), (3,), (2, 2), ()]:
        ndindex_result = list(np.ndindex(shape))
        ndenumerate_indices = [ix for ix, _ in np.ndenumerate(np.zeros(shape))]
        assert_array_equal(ndindex_result, ndenumerate_indices)

