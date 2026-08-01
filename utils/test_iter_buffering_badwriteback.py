
def test_iter_buffering_badwriteback():
    # Writing back from a buffer cannot combine elements

    # a needs write buffering, but had a broadcast dimension
    a = np.arange(6).reshape(2, 3, 1)
    b = np.arange(12).reshape(2, 3, 2)
    assert_raises(ValueError, nditer, [a, b],
                  ['buffered', 'external_loop'],
                  [['readwrite'], ['writeonly']],
                  order='C')

    # But if a is readonly, it's fine
    nditer([a, b], ['buffered', 'external_loop'],
           [['readonly'], ['writeonly']],
           order='C')

    # If a has just one element, it's fine too (constant 0 stride, a reduction)
    a = np.arange(1).reshape(1, 1, 1)
    nditer([a, b], ['buffered', 'external_loop', 'reduce_ok'],
           [['readwrite'], ['writeonly']],
           order='C')

    # check that it fails on other dimensions too
    a = np.arange(6).reshape(1, 3, 2)
    assert_raises(ValueError, nditer, [a, b],
                  ['buffered', 'external_loop'],
                  [['readwrite'], ['writeonly']],
                  order='C')
    a = np.arange(4).reshape(2, 1, 2)
    assert_raises(ValueError, nditer, [a, b],
                  ['buffered', 'external_loop'],
                  [['readwrite'], ['writeonly']],
                  order='C')

