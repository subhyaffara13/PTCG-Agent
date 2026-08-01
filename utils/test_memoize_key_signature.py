
def test_memoize_key_signature():
    # Single argument should not be tupled as a key.  No keywords.
    mf = memoize(lambda x: False, cache={1: True})
    assert mf(1) is True
    assert mf(2) is False

    # Single argument must be tupled if signature has varargs.  No keywords.
    mf = memoize(lambda x, *args: False, cache={(1,): True, (1, 2): 2})
    assert mf(1) is True
    assert mf(2) is False
    assert mf(1, 1) is False
    assert mf(1, 2) == 2
    assert mf((1, 2)) is False

    # More than one argument is always tupled.  No keywords.
    mf = memoize(lambda x, y: False, cache={(1, 2): True})
    assert mf(1, 2) is True
    assert mf(1, 3) is False
    assert raises(TypeError, lambda: mf((1, 2)))

    # Nullary function (no inputs) uses empty tuple as the key
    mf = memoize(lambda: False, cache={(): True})
    assert mf() is True

    # Single argument must be tupled if there are keyword arguments, because
    # keyword arguments may be passed as unnamed args.
    mf = memoize(lambda x, y=0: False,
                 cache={((1,), frozenset((('y', 2),))): 2,
                        ((1, 2), None): 3})
    assert mf(1, y=2) == 2
    assert mf(1, 2) == 3
    assert mf(2, y=2) is False
    assert mf(2, 2) is False
    assert mf(1) is False
    assert mf((1, 2)) is False

    # Keyword-only signatures must still have an "args" tuple.
    mf = memoize(lambda x=0: False, cache={(None, frozenset((('x', 1),))): 1,
                                           ((1,), None): 2})
    assert mf() is False
    assert mf(x=1) == 1
    assert mf(1) == 2

