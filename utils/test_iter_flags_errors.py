
def test_iter_flags_errors():
    # Check that bad combinations of flags produce errors

    a = arange(6)

    # Not enough operands
    assert_raises(ValueError, nditer, [], [], [])
    # Bad global flag
    assert_raises(ValueError, nditer, [a], ['bad flag'], [['readonly']])
    # Bad op flag
    assert_raises(ValueError, nditer, [a], [], [['readonly', 'bad flag']])
    # Bad order parameter
    assert_raises(ValueError, nditer, [a], [], [['readonly']], order='G')
    # Bad casting parameter
    assert_raises(ValueError, nditer, [a], [], [['readonly']], casting='noon')
    # op_flags must match ops
    assert_raises(ValueError, nditer, [a] * 3, [], [['readonly']] * 2)
    # Cannot track both a C and an F index
    assert_raises(ValueError, nditer, a,
                ['c_index', 'f_index'], [['readonly']])
    # Inner iteration and multi-indices/indices are incompatible
    assert_raises(ValueError, nditer, a,
                ['external_loop', 'multi_index'], [['readonly']])
    assert_raises(ValueError, nditer, a,
                ['external_loop', 'c_index'], [['readonly']])
    assert_raises(ValueError, nditer, a,
                ['external_loop', 'f_index'], [['readonly']])
    # Must specify exactly one of readwrite/readonly/writeonly per operand
    assert_raises(ValueError, nditer, a, [], [[]])
    assert_raises(ValueError, nditer, a, [], [['readonly', 'writeonly']])
    assert_raises(ValueError, nditer, a, [], [['readonly', 'readwrite']])
    assert_raises(ValueError, nditer, a, [], [['writeonly', 'readwrite']])
    assert_raises(ValueError, nditer, a,
                [], [['readonly', 'writeonly', 'readwrite']])
    # Python scalars are always readonly
    assert_raises(TypeError, nditer, 1.5, [], [['writeonly']])
    assert_raises(TypeError, nditer, 1.5, [], [['readwrite']])
    # Array scalars are always readonly
    assert_raises(TypeError, nditer, np.int32(1), [], [['writeonly']])
    assert_raises(TypeError, nditer, np.int32(1), [], [['readwrite']])
    # Check readonly array
    a.flags.writeable = False
    assert_raises(ValueError, nditer, a, [], [['writeonly']])
    assert_raises(ValueError, nditer, a, [], [['readwrite']])
    a.flags.writeable = True
    # Multi-indices available only with the multi_index flag
    i = nditer(arange(6), [], [['readonly']])
    assert_raises(ValueError, lambda i: i.multi_index, i)
    # Index available only with an index flag
    assert_raises(ValueError, lambda i: i.index, i)
    # GotoCoords and GotoIndex incompatible with buffering or no_inner

    def assign_multi_index(i):
        i.multi_index = (0,)

    def assign_index(i):
        i.index = 0

    def assign_iterindex(i):
        i.iterindex = 0

    def assign_iterrange(i):
        i.iterrange = (0, 1)
    i = nditer(arange(6), ['external_loop'])
    assert_raises(ValueError, assign_multi_index, i)
    assert_raises(ValueError, assign_index, i)
    assert_raises(ValueError, assign_iterindex, i)
    assert_raises(ValueError, assign_iterrange, i)
    i = nditer(arange(6), ['buffered'])
    assert_raises(ValueError, assign_multi_index, i)
    assert_raises(ValueError, assign_index, i)
    assert_raises(ValueError, assign_iterrange, i)
    # Can't iterate if size is zero
    assert_raises(ValueError, nditer, np.array([]))

