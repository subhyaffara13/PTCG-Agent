
def test_iter_scalar_cast_errors():
    # Check that invalid casts are caught

    # Need to allow copying/buffering for write casts of scalars to occur
    assert_raises(TypeError, nditer, np.float32(2), [],
                [['readwrite']], op_dtypes=[np.dtype('f8')])
    assert_raises(TypeError, nditer, 2.5, [],
                [['readwrite']], op_dtypes=[np.dtype('f4')])
    # 'f8' -> 'f4' isn't a safe cast if the value would overflow
    assert_raises(TypeError, nditer, np.float64(1e60), [],
                [['readonly']],
                casting='safe',
                op_dtypes=[np.dtype('f4')])
    # 'f4' -> 'i4' is neither a safe nor a same-kind cast
    assert_raises(TypeError, nditer, np.float32(2), [],
                [['readonly']],
                casting='same_kind',
                op_dtypes=[np.dtype('i4')])

