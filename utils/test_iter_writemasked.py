
def test_iter_writemasked(arrs):
    # Note, the slicing above is to ensure that nditer cannot combine multiple
    # axes into one.  The repetition is just to make things a bit more
    # interesting.
    a = arrs.copy()
    shape = a.shape
    reps = shape[-1] // 3
    msk = np.empty(shape, dtype=bool)
    msk[...] = [True, True, False] * reps

    # When buffering is unused, 'writemasked' effectively does nothing.
    # It's up to the user of the iterator to obey the requested semantics.
    it = np.nditer([a, msk], [],
                [['readwrite', 'writemasked'],
                 ['readonly', 'arraymask']])
    with it:
        for x, m in it:
            x[...] = 1
    # Because we violated the semantics, all the values became 1
    assert_equal(a, np.broadcast_to([1, 1, 1] * reps, shape))

    # Even if buffering is enabled, we still may be accessing the array
    # directly.
    it = np.nditer([a, msk], ['buffered'],
                [['readwrite', 'writemasked'],
                 ['readonly', 'arraymask']])
    # @seberg: I honestly don't currently understand why a "buffered" iterator
    # would end up not using a buffer for the small array here at least when
    # "writemasked" is used, that seems confusing...  Check by testing for
    # actual memory overlap!
    is_buffered = True
    with it:
        for x, m in it:
            x[...] = 2.5
            if np.may_share_memory(x, a):
                is_buffered = False

    if not is_buffered:
        # Because we violated the semantics, all the values became 2.5
        assert_equal(a, np.broadcast_to([2.5, 2.5, 2.5] * reps, shape))
    else:
        # For large sizes, the iterator may be buffered:
        assert_equal(a, np.broadcast_to([2.5, 2.5, 1] * reps, shape))
        a[...] = 2.5

    # If buffering will definitely happening, for instance because of
    # a cast, only the items selected by the mask will be copied back from
    # the buffer.
    it = np.nditer([a, msk], ['buffered'],
                [['readwrite', 'writemasked'],
                 ['readonly', 'arraymask']],
                op_dtypes=['i8', None],
                casting='unsafe')
    with it:
        for x, m in it:
            x[...] = 3
    # Even though we violated the semantics, only the selected values
    # were copied back
    assert_equal(a, np.broadcast_to([3, 3, 2.5] * reps, shape))

