
def test_iter_buffered_cast_simple():
    # Test that buffering can handle a simple cast

    a = np.arange(10, dtype='f4')
    i = nditer(a, ['buffered', 'external_loop'],
                   [['readwrite', 'nbo', 'aligned']],
                   casting='same_kind',
                   op_dtypes=[np.dtype('f8')],
                   buffersize=3)
    with i:
        for v in i:
            v[...] *= 2

    assert_equal(a, 2 * np.arange(10, dtype='f4'))

