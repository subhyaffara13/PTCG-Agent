
def test_iter_broadcasting():
    # Standard NumPy broadcasting rules

    # 1D with scalar
    i = nditer([arange(6), np.int32(2)], ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 6)
    assert_equal(i.shape, (6,))

    # 2D with scalar
    i = nditer([arange(6).reshape(2, 3), np.int32(2)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 6)
    assert_equal(i.shape, (2, 3))
    # 2D with 1D
    i = nditer([arange(6).reshape(2, 3), arange(3)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 6)
    assert_equal(i.shape, (2, 3))
    i = nditer([arange(2).reshape(2, 1), arange(3)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 6)
    assert_equal(i.shape, (2, 3))
    # 2D with 2D
    i = nditer([arange(2).reshape(2, 1), arange(3).reshape(1, 3)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 6)
    assert_equal(i.shape, (2, 3))

    # 3D with scalar
    i = nditer([np.int32(2), arange(24).reshape(4, 2, 3)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 24)
    assert_equal(i.shape, (4, 2, 3))
    # 3D with 1D
    i = nditer([arange(3), arange(24).reshape(4, 2, 3)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 24)
    assert_equal(i.shape, (4, 2, 3))
    i = nditer([arange(3), arange(8).reshape(4, 2, 1)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 24)
    assert_equal(i.shape, (4, 2, 3))
    # 3D with 2D
    i = nditer([arange(6).reshape(2, 3), arange(24).reshape(4, 2, 3)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 24)
    assert_equal(i.shape, (4, 2, 3))
    i = nditer([arange(2).reshape(2, 1), arange(24).reshape(4, 2, 3)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 24)
    assert_equal(i.shape, (4, 2, 3))
    i = nditer([arange(3).reshape(1, 3), arange(8).reshape(4, 2, 1)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 24)
    assert_equal(i.shape, (4, 2, 3))
    # 3D with 3D
    i = nditer([arange(2).reshape(1, 2, 1), arange(3).reshape(1, 1, 3),
                        arange(4).reshape(4, 1, 1)],
                        ['multi_index'], [['readonly']] * 3)
    assert_equal(i.itersize, 24)
    assert_equal(i.shape, (4, 2, 3))
    i = nditer([arange(6).reshape(1, 2, 3), arange(4).reshape(4, 1, 1)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 24)
    assert_equal(i.shape, (4, 2, 3))
    i = nditer([arange(24).reshape(4, 2, 3), arange(12).reshape(4, 1, 3)],
                        ['multi_index'], [['readonly']] * 2)
    assert_equal(i.itersize, 24)
    assert_equal(i.shape, (4, 2, 3))

