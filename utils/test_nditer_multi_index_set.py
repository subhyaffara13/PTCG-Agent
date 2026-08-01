
def test_nditer_multi_index_set():
    # Test the multi_index set
    a = np.arange(6).reshape(2, 3)
    it = np.nditer(a, flags=['multi_index'])

    # Removes the iteration on two first elements of a[0]
    it.multi_index = (0, 2,)

    assert_equal(list(it), [2, 3, 4, 5])

