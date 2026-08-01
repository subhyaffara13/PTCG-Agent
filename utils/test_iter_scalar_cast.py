
def test_iter_scalar_cast():
    # Check that scalars are cast as requested

    # No cast 'f4' -> 'f4'
    i = nditer(np.float32(2.5), [], [['readonly']],
                    op_dtypes=[np.dtype('f4')])
    assert_equal(i.dtypes[0], np.dtype('f4'))
    assert_equal(i.value.dtype, np.dtype('f4'))
    assert_equal(i.value, 2.5)
    # Safe cast 'f4' -> 'f8'
    i = nditer(np.float32(2.5), [],
                    [['readonly', 'copy']],
                    casting='safe',
                    op_dtypes=[np.dtype('f8')])
    assert_equal(i.dtypes[0], np.dtype('f8'))
    assert_equal(i.value.dtype, np.dtype('f8'))
    assert_equal(i.value, 2.5)
    # Same-kind cast 'f8' -> 'f4'
    i = nditer(np.float64(2.5), [],
                    [['readonly', 'copy']],
                    casting='same_kind',
                    op_dtypes=[np.dtype('f4')])
    assert_equal(i.dtypes[0], np.dtype('f4'))
    assert_equal(i.value.dtype, np.dtype('f4'))
    assert_equal(i.value, 2.5)
    # Unsafe cast 'f8' -> 'i4'
    i = nditer(np.float64(3.0), [],
                    [['readonly', 'copy']],
                    casting='unsafe',
                    op_dtypes=[np.dtype('i4')])
    assert_equal(i.dtypes[0], np.dtype('i4'))
    assert_equal(i.value.dtype, np.dtype('i4'))
    assert_equal(i.value, 3)
    # Readonly scalars may be cast even without setting COPY or BUFFERED
    i = nditer(3, [], [['readonly']], op_dtypes=[np.dtype('f8')])
    assert_equal(i[0].dtype, np.dtype('f8'))
    assert_equal(i[0], 3.)

