
def test_iter_buffered_cast_byteswapped_complex():
    # Test that buffering can handle a cast which requires swap->cast->copy

    a = np.arange(10, dtype='c8')
    a = a.view(a.dtype.newbyteorder()).byteswap()
    a += 2j
    i = nditer(a, ['buffered', 'external_loop'],
                   [['readwrite', 'nbo', 'aligned']],
                   casting='same_kind',
                   op_dtypes=[np.dtype('c16')],
                   buffersize=3)
    with i:
        for v in i:
            v[...] *= 2
    assert_equal(a, 2 * np.arange(10, dtype='c8') + 4j)

    a = np.arange(10, dtype='c8')
    a += 2j
    i = nditer(a, ['buffered', 'external_loop'],
                   [['readwrite', 'nbo', 'aligned']],
                   casting='same_kind',
                   op_dtypes=[np.dtype('c16').newbyteorder()],
                   buffersize=3)
    with i:
        for v in i:
            v[...] *= 2
    assert_equal(a, 2 * np.arange(10, dtype='c8') + 4j)

    a = np.arange(10, dtype=np.clongdouble)
    a = a.view(a.dtype.newbyteorder()).byteswap()
    a += 2j
    i = nditer(a, ['buffered', 'external_loop'],
                   [['readwrite', 'nbo', 'aligned']],
                   casting='same_kind',
                   op_dtypes=[np.dtype('c16')],
                   buffersize=3)
    with i:
        for v in i:
            v[...] *= 2
    assert_equal(a, 2 * np.arange(10, dtype=np.clongdouble) + 4j)

    a = np.arange(10, dtype=np.longdouble)
    a = a.view(a.dtype.newbyteorder()).byteswap()
    i = nditer(a, ['buffered', 'external_loop'],
                   [['readwrite', 'nbo', 'aligned']],
                   casting='same_kind',
                   op_dtypes=[np.dtype('f4')],
                   buffersize=7)
    with i:
        for v in i:
            v[...] *= 2
    assert_equal(a, 2 * np.arange(10, dtype=np.longdouble))

