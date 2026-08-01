
def test_iter_op_axes():
    # Check that custom axes work

    # Reverse the axes
    a = arange(6).reshape(2, 3)
    i = nditer([a, a.T], [], [['readonly']] * 2, op_axes=[[0, 1], [1, 0]])
    assert_(all([x == y for (x, y) in i]))
    a = arange(24).reshape(2, 3, 4)
    i = nditer([a.T, a], [], [['readonly']] * 2, op_axes=[[2, 1, 0], None])
    assert_(all([x == y for (x, y) in i]))

    # Broadcast 1D to any dimension
    a = arange(1, 31).reshape(2, 3, 5)
    b = arange(1, 3)
    i = nditer([a, b], [], [['readonly']] * 2, op_axes=[None, [0, -1, -1]])
    assert_equal([x * y for (x, y) in i], (a * b.reshape(2, 1, 1)).ravel())
    b = arange(1, 4)
    i = nditer([a, b], [], [['readonly']] * 2, op_axes=[None, [-1, 0, -1]])
    assert_equal([x * y for (x, y) in i], (a * b.reshape(1, 3, 1)).ravel())
    b = arange(1, 6)
    i = nditer([a, b], [], [['readonly']] * 2,
                            op_axes=[None, [np.newaxis, np.newaxis, 0]])
    assert_equal([x * y for (x, y) in i], (a * b.reshape(1, 1, 5)).ravel())

    # Inner product-style broadcasting
    a = arange(24).reshape(2, 3, 4)
    b = arange(40).reshape(5, 2, 4)
    i = nditer([a, b], ['multi_index'], [['readonly']] * 2,
                            op_axes=[[0, 1, -1, -1], [-1, -1, 0, 1]])
    assert_equal(i.shape, (2, 3, 5, 2))

    # Matrix product-style broadcasting
    a = arange(12).reshape(3, 4)
    b = arange(20).reshape(4, 5)
    i = nditer([a, b], ['multi_index'], [['readonly']] * 2,
                            op_axes=[[0, -1], [-1, 1]])
    assert_equal(i.shape, (3, 5))

