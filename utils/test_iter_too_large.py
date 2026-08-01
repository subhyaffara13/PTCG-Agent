
def test_iter_too_large():
    # The total size of the iterator must not exceed the maximum intp due
    # to broadcasting. Dividing by 1024 will keep it small enough to
    # give a legal array.
    size = np.iinfo(np.intp).max // 1024
    arr = np.lib.stride_tricks.as_strided(np.zeros(1), (size,), (0,))
    assert_raises(ValueError, nditer, (arr, arr[:, None]))
    # test the same for multiindex. That may get more interesting when
    # removing 0 dimensional axis is allowed (since an iterator can grow then)
    assert_raises(ValueError, nditer,
                  (arr, arr[:, None]), flags=['multi_index'])

