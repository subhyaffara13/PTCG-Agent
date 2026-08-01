
def test_iter_allocate_output_itorder():
    # The allocated output should match the iteration order

    # C-order input, best iteration order
    a = arange(6, dtype='i4').reshape(2, 3)
    i = nditer([a, None], [], [['readonly'], ['writeonly', 'allocate']],
                        op_dtypes=[None, np.dtype('f4')])
    assert_equal(i.operands[1].shape, a.shape)
    assert_equal(i.operands[1].strides, a.strides)
    assert_equal(i.operands[1].dtype, np.dtype('f4'))
    # F-order input, best iteration order
    a = arange(24, dtype='i4').reshape(2, 3, 4).T
    i = nditer([a, None], [], [['readonly'], ['writeonly', 'allocate']],
                        op_dtypes=[None, np.dtype('f4')])
    assert_equal(i.operands[1].shape, a.shape)
    assert_equal(i.operands[1].strides, a.strides)
    assert_equal(i.operands[1].dtype, np.dtype('f4'))
    # Non-contiguous input, C iteration order
    a = arange(24, dtype='i4').reshape(2, 3, 4).swapaxes(0, 1)
    i = nditer([a, None], [],
                        [['readonly'], ['writeonly', 'allocate']],
                        order='C',
                        op_dtypes=[None, np.dtype('f4')])
    assert_equal(i.operands[1].shape, a.shape)
    assert_equal(i.operands[1].strides, (32, 16, 4))
    assert_equal(i.operands[1].dtype, np.dtype('f4'))

