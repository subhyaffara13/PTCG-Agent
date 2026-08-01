
def test_iter_broadcasting_errors():
    # Check that errors are thrown for bad broadcasting shapes

    # 1D with 1D
    assert_raises(ValueError, nditer, [arange(2), arange(3)],
                    [], [['readonly']] * 2)
    # 2D with 1D
    assert_raises(ValueError, nditer,
                    [arange(6).reshape(2, 3), arange(2)],
                    [], [['readonly']] * 2)
    # 2D with 2D
    assert_raises(ValueError, nditer,
                    [arange(6).reshape(2, 3), arange(9).reshape(3, 3)],
                    [], [['readonly']] * 2)
    assert_raises(ValueError, nditer,
                    [arange(6).reshape(2, 3), arange(4).reshape(2, 2)],
                    [], [['readonly']] * 2)
    # 3D with 3D
    assert_raises(ValueError, nditer,
                    [arange(36).reshape(3, 3, 4), arange(24).reshape(2, 3, 4)],
                    [], [['readonly']] * 2)
    assert_raises(ValueError, nditer,
                    [arange(8).reshape(2, 4, 1), arange(24).reshape(2, 3, 4)],
                    [], [['readonly']] * 2)

    # Verify that the error message mentions the right shapes
    try:
        nditer([arange(2).reshape(1, 2, 1),
                arange(3).reshape(1, 3),
                arange(6).reshape(2, 3)],
               [],
               [['readonly'], ['readonly'], ['writeonly', 'no_broadcast']])
        raise AssertionError('Should have raised a broadcast error')
    except ValueError as e:
        msg = str(e)
        # The message should contain the shape of the 3rd operand
        assert_(msg.find('(2,3)') >= 0,
                f'Message "{msg}" doesn\'t contain operand shape (2,3)')
        # The message should contain the broadcast shape
        assert_(msg.find('(1,2,3)') >= 0,
                f'Message "{msg}" doesn\'t contain broadcast shape (1,2,3)')

    try:
        nditer([arange(6).reshape(2, 3), arange(2)],
               [],
               [['readonly'], ['readonly']],
               op_axes=[[0, 1], [0, np.newaxis]],
               itershape=(4, 3))
        raise AssertionError('Should have raised a broadcast error')
    except ValueError as e:
        msg = str(e)
        # The message should contain "shape->remappedshape" for each operand
        assert_(msg.find('(2,3)->(2,3)') >= 0,
            f'Message "{msg}" doesn\'t contain operand shape (2,3)->(2,3)')
        assert_(msg.find('(2,)->(2,newaxis)') >= 0,
                f'Message "{msg}" doesn\'t contain remapped operand shape'
                '(2,)->(2,newaxis)')
        # The message should contain the itershape parameter
        assert_(msg.find('(4,3)') >= 0,
                f'Message "{msg}" doesn\'t contain itershape parameter (4,3)')

    try:
        nditer([np.zeros((2, 1, 1)), np.zeros((2,))],
               [],
               [['writeonly', 'no_broadcast'], ['readonly']])
        raise AssertionError('Should have raised a broadcast error')
    except ValueError as e:
        msg = str(e)
        # The message should contain the shape of the bad operand
        assert_(msg.find('(2,1,1)') >= 0,
            f'Message "{msg}" doesn\'t contain operand shape (2,1,1)')
        # The message should contain the broadcast shape
        assert_(msg.find('(2,1,2)') >= 0,
                f'Message "{msg}" doesn\'t contain the broadcast shape (2,1,2)')

