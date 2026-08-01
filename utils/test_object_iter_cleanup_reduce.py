
def test_object_iter_cleanup_reduce():
    # Similar as above, but a complex reduction case that was previously
    # missed (see gh-18810).
    # The following array is special in that it cannot be flattened:
    arr = np.array([[None, 1], [-1, -1], [None, 2], [-1, -1]])[::2]
    with pytest.raises(TypeError):
        np.sum(arr)

