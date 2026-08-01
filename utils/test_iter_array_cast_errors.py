
def test_iter_array_cast_errors():
    # Check that invalid casts are caught

    # Need to enable copying for casts to occur
    assert_raises(TypeError, nditer, arange(2, dtype='f4'), [],
                [['readonly']], op_dtypes=[np.dtype('f8')])
    # Also need to allow casting for casts to occur
    assert_raises(TypeError, nditer, arange(2, dtype='f4'), [],
                [['readonly', 'copy']], casting='no',
                op_dtypes=[np.dtype('f8')])
    assert_raises(TypeError, nditer, arange(2, dtype='f4'), [],
                [['readonly', 'copy']], casting='equiv',
                op_dtypes=[np.dtype('f8')])
    assert_raises(TypeError, nditer, arange(2, dtype='f8'), [],
                [['writeonly', 'updateifcopy']],
                casting='no',
                op_dtypes=[np.dtype('f4')])
    assert_raises(TypeError, nditer, arange(2, dtype='f8'), [],
                [['writeonly', 'updateifcopy']],
                casting='equiv',
                op_dtypes=[np.dtype('f4')])
    # '<f4' -> '>f4' should not work with casting='no'
    assert_raises(TypeError, nditer, arange(2, dtype='<f4'), [],
                [['readonly', 'copy']], casting='no',
                op_dtypes=[np.dtype('>f4')])
    # 'f4' -> 'f8' is a safe cast, but 'f8' -> 'f4' isn't
    assert_raises(TypeError, nditer, arange(2, dtype='f4'), [],
                [['readwrite', 'updateifcopy']],
                casting='safe',
                op_dtypes=[np.dtype('f8')])
    assert_raises(TypeError, nditer, arange(2, dtype='f8'), [],
                [['readwrite', 'updateifcopy']],
                casting='safe',
                op_dtypes=[np.dtype('f4')])
    # 'f4' -> 'i4' is neither a safe nor a same-kind cast
    assert_raises(TypeError, nditer, arange(2, dtype='f4'), [],
                [['readonly', 'copy']],
                casting='same_kind',
                op_dtypes=[np.dtype('i4')])
    assert_raises(TypeError, nditer, arange(2, dtype='i4'), [],
                [['writeonly', 'updateifcopy']],
                casting='same_kind',
                op_dtypes=[np.dtype('f4')])

