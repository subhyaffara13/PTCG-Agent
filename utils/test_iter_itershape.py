
def test_iter_itershape():
    # Check that allocated outputs work with a specified shape
    a = np.arange(6, dtype='i2').reshape(2, 3)
    i = nditer([a, None], [], [['readonly'], ['writeonly', 'allocate']],
                            op_axes=[[0, 1, None], None],
                            itershape=(-1, -1, 4))
    assert_equal(i.operands[1].shape, (2, 3, 4))
    assert_equal(i.operands[1].strides, (24, 8, 2))

    i = nditer([a.T, None], [], [['readonly'], ['writeonly', 'allocate']],
                            op_axes=[[0, 1, None], None],
                            itershape=(-1, -1, 4))
    assert_equal(i.operands[1].shape, (3, 2, 4))
    assert_equal(i.operands[1].strides, (8, 24, 2))

    i = nditer([a.T, None], [], [['readonly'], ['writeonly', 'allocate']],
                            order='F',
                            op_axes=[[0, 1, None], None],
                            itershape=(-1, -1, 4))
    assert_equal(i.operands[1].shape, (3, 2, 4))
    assert_equal(i.operands[1].strides, (2, 6, 12))

    # If we specify 1 in the itershape, it shouldn't allow broadcasting
    # of that dimension to a bigger value
    assert_raises(ValueError, nditer, [a, None], [],
                            [['readonly'], ['writeonly', 'allocate']],
                            op_axes=[[0, 1, None], None],
                            itershape=(-1, 1, 4))
    # Test bug that for no op_axes but itershape, they are NULLed correctly
    i = np.nditer([np.ones(2), None, None], itershape=(2,))

