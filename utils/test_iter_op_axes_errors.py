
def test_iter_op_axes_errors():
    # Check that custom axes throws errors for bad inputs

    # Wrong number of items in op_axes
    a = arange(6).reshape(2, 3)
    assert_raises(ValueError, nditer, [a, a], [], [['readonly']] * 2,
                                    op_axes=[[0], [1], [0]])
    # Out of bounds items in op_axes
    assert_raises(ValueError, nditer, [a, a], [], [['readonly']] * 2,
                                    op_axes=[[2, 1], [0, 1]])
    assert_raises(ValueError, nditer, [a, a], [], [['readonly']] * 2,
                                    op_axes=[[0, 1], [2, -1]])
    # Duplicate items in op_axes
    assert_raises(ValueError, nditer, [a, a], [], [['readonly']] * 2,
                                    op_axes=[[0, 0], [0, 1]])
    assert_raises(ValueError, nditer, [a, a], [], [['readonly']] * 2,
                                    op_axes=[[0, 1], [1, 1]])

    # Different sized arrays in op_axes
    assert_raises(ValueError, nditer, [a, a], [], [['readonly']] * 2,
                                    op_axes=[[0, 1], [0, 1, 0]])

    # Non-broadcastable dimensions in the result
    assert_raises(ValueError, nditer, [a, a], [], [['readonly']] * 2,
                                    op_axes=[[0, 1], [1, 0]])

