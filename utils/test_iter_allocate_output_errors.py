
def test_iter_allocate_output_errors():
    # Check that the iterator will throw errors for bad output allocations

    # Need an input if no output data type is specified
    a = arange(6)
    assert_raises(TypeError, nditer, [a, None], [],
                        [['writeonly'], ['writeonly', 'allocate']])
    # Allocated output should be flagged for writing
    assert_raises(ValueError, nditer, [a, None], [],
                        [['readonly'], ['allocate', 'readonly']])
    # Allocated output can't have buffering without delayed bufalloc
    assert_raises(ValueError, nditer, [a, None], ['buffered'],
                                            ['allocate', 'readwrite'])
    # Must specify dtype if there are no inputs (cannot promote existing ones;
    # maybe this should use the 'f4' here, but it does not historically.)
    assert_raises(TypeError, nditer, [None, None], [],
                        [['writeonly', 'allocate'],
                         ['writeonly', 'allocate']],
                        op_dtypes=[None, np.dtype('f4')])
    # If using op_axes, must specify all the axes
    a = arange(24, dtype='i4').reshape(2, 3, 4)
    assert_raises(ValueError, nditer, [a, None], [],
                        [['readonly'], ['writeonly', 'allocate']],
                        op_dtypes=[None, np.dtype('f4')],
                        op_axes=[None, [0, np.newaxis, 1]])
    # If using op_axes, the axes must be within bounds
    assert_raises(ValueError, nditer, [a, None], [],
                        [['readonly'], ['writeonly', 'allocate']],
                        op_dtypes=[None, np.dtype('f4')],
                        op_axes=[None, [0, 3, 1]])
    # If using op_axes, there can't be duplicates
    assert_raises(ValueError, nditer, [a, None], [],
                        [['readonly'], ['writeonly', 'allocate']],
                        op_dtypes=[None, np.dtype('f4')],
                        op_axes=[None, [0, 2, 1, 0]])
    # Not all axes may be specified if a reduction. If there is a hole
    # in op_axes, this is an error.
    a = arange(24, dtype='i4').reshape(2, 3, 4)
    assert_raises(ValueError, nditer, [a, None], ["reduce_ok"],
                        [['readonly'], ['readwrite', 'allocate']],
                        op_dtypes=[None, np.dtype('f4')],
                        op_axes=[None, [0, np.newaxis, 2]])

