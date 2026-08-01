
def test_nditer_multi_index_set_refcount():
    # Test if the reference count on index variable is decreased

    index = 0
    i = np.nditer(np.array([111, 222, 333, 444]), flags=['multi_index'])

    start_count = sys.getrefcount(index)
    i.multi_index = (index,)
    end_count = sys.getrefcount(index)

    assert_equal(start_count, end_count)

