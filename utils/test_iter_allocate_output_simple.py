
def test_iter_allocate_output_simple():
    # Check that the iterator will properly allocate outputs

    # Simple case
    a = arange(6)
    i = nditer([a, None], [], [['readonly'], ['writeonly', 'allocate']],
                        op_dtypes=[None, np.dtype('f4')])
    assert_equal(i.operands[1].shape, a.shape)
    assert_equal(i.operands[1].dtype, np.dtype('f4'))

