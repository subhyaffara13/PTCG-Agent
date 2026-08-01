
def test_iter_writemasked_badinput():
    a = np.zeros((2, 3))
    b = np.zeros((3,))
    m = np.array([[True, True, False], [False, True, False]])
    m2 = np.array([True, True, False])
    m3 = np.array([0, 1, 1], dtype='u1')
    mbad1 = np.array([0, 1, 1], dtype='i1')
    mbad2 = np.array([0, 1, 1], dtype='f4')

    # Need an 'arraymask' if any operand is 'writemasked'
    assert_raises(ValueError, nditer, [a, m], [],
                    [['readwrite', 'writemasked'], ['readonly']])

    # A 'writemasked' operand must not be readonly
    assert_raises(ValueError, nditer, [a, m], [],
                    [['readonly', 'writemasked'], ['readonly', 'arraymask']])

    # 'writemasked' and 'arraymask' may not be used together
    assert_raises(ValueError, nditer, [a, m], [],
                    [['readonly'], ['readwrite', 'arraymask', 'writemasked']])

    # 'arraymask' may only be specified once
    assert_raises(ValueError, nditer, [a, m, m2], [],
                    [['readwrite', 'writemasked'],
                     ['readonly', 'arraymask'],
                     ['readonly', 'arraymask']])

    # An 'arraymask' with nothing 'writemasked' also doesn't make sense
    assert_raises(ValueError, nditer, [a, m], [],
                    [['readwrite'], ['readonly', 'arraymask']])

    # A writemasked reduction requires a similarly smaller mask
    assert_raises(ValueError, nditer, [a, b, m], ['reduce_ok'],
                    [['readonly'],
                     ['readwrite', 'writemasked'],
                     ['readonly', 'arraymask']])
    # But this should work with a smaller/equal mask to the reduction operand
    np.nditer([a, b, m2], ['reduce_ok'],
                    [['readonly'],
                     ['readwrite', 'writemasked'],
                     ['readonly', 'arraymask']])
    # The arraymask itself cannot be a reduction
    assert_raises(ValueError, nditer, [a, b, m2], ['reduce_ok'],
                    [['readonly'],
                     ['readwrite', 'writemasked'],
                     ['readwrite', 'arraymask']])

    # A uint8 mask is ok too
    np.nditer([a, m3], ['buffered'],
                    [['readwrite', 'writemasked'],
                     ['readonly', 'arraymask']],
                    op_dtypes=['f4', None],
                    casting='same_kind')
    # An int8 mask isn't ok
    assert_raises(TypeError, np.nditer, [a, mbad1], ['buffered'],
                    [['readwrite', 'writemasked'],
                     ['readonly', 'arraymask']],
                    op_dtypes=['f4', None],
                    casting='same_kind')
    # A float32 mask isn't ok
    assert_raises(TypeError, np.nditer, [a, mbad2], ['buffered'],
                    [['readwrite', 'writemasked'],
                     ['readonly', 'arraymask']],
                    op_dtypes=['f4', None],
                    casting='same_kind')

