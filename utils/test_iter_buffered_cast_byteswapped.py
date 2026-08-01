
def test_iter_buffered_cast_byteswapped():
    # Test that buffering can handle a cast which requires swap->cast->swap

    a = np.arange(10, dtype='f4')
    a = a.view(a.dtype.newbyteorder()).byteswap()
    i = nditer(a, ['buffered', 'external_loop'],
                   [['readwrite', 'nbo', 'aligned']],
                   casting='same_kind',
                   op_dtypes=[np.dtype('f8').newbyteorder()],
                   buffersize=3)
    with i:
        for v in i:
            v[...] *= 2

    assert_equal(a, 2 * np.arange(10, dtype='f4'))

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', np.exceptions.ComplexWarning)

        a = np.arange(10, dtype='f8')
        a = a.view(a.dtype.newbyteorder()).byteswap()
        i = nditer(a, ['buffered', 'external_loop'],
                       [['readwrite', 'nbo', 'aligned']],
                       casting='unsafe',
                       op_dtypes=[np.dtype('c8').newbyteorder()],
                       buffersize=3)
        with i:
            for v in i:
                v[...] *= 2

        assert_equal(a, 2 * np.arange(10, dtype='f8'))

