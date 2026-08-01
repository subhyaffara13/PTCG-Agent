
def test_mask_indices():
    # simple test without offset
    iu = mask_indices(3, np.triu)
    a = np.arange(9).reshape(3, 3)
    assert_array_equal(a[iu], array([0, 1, 2, 4, 5, 8]))
    # Now with an offset
    iu1 = mask_indices(3, np.triu, 1)
    assert_array_equal(a[iu1], array([1, 2, 5]))

