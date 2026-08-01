
def test_iter_array_cast():
    # Check that arrays are cast as requested

    # No cast 'f4' -> 'f4'
    a = np.arange(6, dtype='f4').reshape(2, 3)
    i = nditer(a, [], [['readwrite']], op_dtypes=[np.dtype('f4')])
    with i:
        assert_equal(i.operands[0], a)
        assert_equal(i.operands[0].dtype, np.dtype('f4'))

    # Byte-order cast '<f4' -> '>f4'
    a = np.arange(6, dtype='<f4').reshape(2, 3)
    with nditer(a, [], [['readwrite', 'updateifcopy']],
            casting='equiv',
            op_dtypes=[np.dtype('>f4')]) as i:
        assert_equal(i.operands[0], a)
        assert_equal(i.operands[0].dtype, np.dtype('>f4'))

    # Safe case 'f4' -> 'f8'
    a = np.arange(24, dtype='f4').reshape(2, 3, 4).swapaxes(1, 2)
    i = nditer(a, [], [['readonly', 'copy']],
            casting='safe',
            op_dtypes=[np.dtype('f8')])
    assert_equal(i.operands[0], a)
    assert_equal(i.operands[0].dtype, np.dtype('f8'))
    # The memory layout of the temporary should match a (a is (48,4,16))
    # except negative strides get flipped to positive strides.
    assert_equal(i.operands[0].strides, (96, 8, 32))
    a = a[::-1, :, ::-1]
    i = nditer(a, [], [['readonly', 'copy']],
            casting='safe',
            op_dtypes=[np.dtype('f8')])
    assert_equal(i.operands[0], a)
    assert_equal(i.operands[0].dtype, np.dtype('f8'))
    assert_equal(i.operands[0].strides, (96, 8, 32))

    # Same-kind cast 'f8' -> 'f4' -> 'f8'
    a = np.arange(24, dtype='f8').reshape(2, 3, 4).T
    with nditer(a, [],
            [['readwrite', 'updateifcopy']],
            casting='same_kind',
            op_dtypes=[np.dtype('f4')]) as i:
        assert_equal(i.operands[0], a)
        assert_equal(i.operands[0].dtype, np.dtype('f4'))
        assert_equal(i.operands[0].strides, (4, 16, 48))
        # Check that WRITEBACKIFCOPY is activated at exit
        i.operands[0][2, 1, 1] = -12.5
        assert_(a[2, 1, 1] != -12.5)
    assert_equal(a[2, 1, 1], -12.5)

    a = np.arange(6, dtype='i4')[::-2]
    with nditer(a, [],
            [['writeonly', 'updateifcopy']],
            casting='unsafe',
            op_dtypes=[np.dtype('f4')]) as i:
        assert_equal(i.operands[0].dtype, np.dtype('f4'))
        # Even though the stride was negative in 'a', it
        # becomes positive in the temporary
        assert_equal(i.operands[0].strides, (4,))
        i.operands[0][:] = [1, 2, 3]
    assert_equal(a, [1, 2, 3])

