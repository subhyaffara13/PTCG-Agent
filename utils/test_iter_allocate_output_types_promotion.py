
def test_iter_allocate_output_types_promotion():
    # Check type promotion of automatic outputs (this was more interesting
    # before NEP 50...)

    i = nditer([array([3], dtype='f4'), array([0], dtype='f8'), None], [],
                    [['readonly']] * 2 + [['writeonly', 'allocate']])
    assert_equal(i.dtypes[2], np.dtype('f8'))
    i = nditer([array([3], dtype='i4'), array([0], dtype='f4'), None], [],
                    [['readonly']] * 2 + [['writeonly', 'allocate']])
    assert_equal(i.dtypes[2], np.dtype('f8'))
    i = nditer([array([3], dtype='f4'), array(0, dtype='f8'), None], [],
                    [['readonly']] * 2 + [['writeonly', 'allocate']])
    assert_equal(i.dtypes[2], np.dtype('f8'))
    i = nditer([array([3], dtype='u4'), array(0, dtype='i4'), None], [],
                    [['readonly']] * 2 + [['writeonly', 'allocate']])
    assert_equal(i.dtypes[2], np.dtype('i8'))
    i = nditer([array([3], dtype='u4'), array(-12, dtype='i4'), None], [],
                    [['readonly']] * 2 + [['writeonly', 'allocate']])
    assert_equal(i.dtypes[2], np.dtype('i8'))

