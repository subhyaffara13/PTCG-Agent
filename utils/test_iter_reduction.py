
def test_iter_reduction():
    # Test doing reductions with the iterator

    a = np.arange(6)
    i = nditer([a, None], ['reduce_ok'],
                    [['readonly'], ['readwrite', 'allocate']],
                    op_axes=[[0], [-1]])
    # Need to initialize the output operand to the addition unit
    with i:
        i.operands[1][...] = 0
        # Do the reduction
        for x, y in i:
            y[...] += x
        # Since no axes were specified, should have allocated a scalar
        assert_equal(i.operands[1].ndim, 0)
        assert_equal(i.operands[1], np.sum(a))

    a = np.arange(6).reshape(2, 3)
    i = nditer([a, None], ['reduce_ok', 'external_loop'],
                    [['readonly'], ['readwrite', 'allocate']],
                    op_axes=[[0, 1], [-1, -1]])
    # Need to initialize the output operand to the addition unit
    with i:
        i.operands[1][...] = 0
        # Reduction shape/strides for the output
        assert_equal(i[1].shape, (6,))
        assert_equal(i[1].strides, (0,))
        # Do the reduction
        for x, y in i:
            # Use a for loop instead of ``y[...] += x``
            # (equivalent to ``y[...] = y[...].copy() + x``),
            # because y has zero strides we use for the reduction
            for j in range(len(y)):
                y[j] += x[j]
        # Since no axes were specified, should have allocated a scalar
        assert_equal(i.operands[1].ndim, 0)
        assert_equal(i.operands[1], np.sum(a))

    # This is a tricky reduction case for the buffering double loop
    # to handle
    a = np.ones((2, 3, 5))
    it1 = nditer([a, None], ['reduce_ok', 'external_loop'],
                    [['readonly'], ['readwrite', 'allocate']],
                    op_axes=[None, [0, -1, 1]])
    it2 = nditer([a, None], ['reduce_ok', 'external_loop',
                            'buffered', 'delay_bufalloc'],
                    [['readonly'], ['readwrite', 'allocate']],
                    op_axes=[None, [0, -1, 1]], buffersize=10)
    with it1, it2:
        it1.operands[1].fill(0)
        it2.operands[1].fill(0)
        it2.reset()
        for x in it1:
            x[1][...] += x[0]
        for x in it2:
            x[1][...] += x[0]
        assert_equal(it1.operands[1], it2.operands[1])
        assert_equal(it2.operands[1].sum(), a.size)

