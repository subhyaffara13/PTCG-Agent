
def test_iter_allocate_output_opaxes():
    # Specifying op_axes should work

    a = arange(24, dtype='i4').reshape(2, 3, 4)
    i = nditer([None, a], [], [['writeonly', 'allocate'], ['readonly']],
                        op_dtypes=[np.dtype('u4'), None],
                        op_axes=[[1, 2, 0], None])
    assert_equal(i.operands[0].shape, (4, 2, 3))
    assert_equal(i.operands[0].strides, (4, 48, 16))
    assert_equal(i.operands[0].dtype, np.dtype('u4'))

