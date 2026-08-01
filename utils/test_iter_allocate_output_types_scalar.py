
def test_iter_allocate_output_types_scalar():
    # If the inputs are all scalars, the output should be a scalar

    i = nditer([None, 1, 2.3, np.float32(12), np.complex128(3)], [],
                [['writeonly', 'allocate']] + [['readonly']] * 4)
    assert_equal(i.operands[0].dtype, np.dtype('complex128'))
    assert_equal(i.operands[0].ndim, 0)

