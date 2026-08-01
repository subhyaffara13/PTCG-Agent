
def test_writebacks():
    a = np.arange(6, dtype='f4')
    au = a.byteswap()
    au = au.view(au.dtype.newbyteorder())
    assert_(a.dtype.byteorder != au.dtype.byteorder)
    it = nditer(au, [], [['readwrite', 'updateifcopy']],
                        casting='equiv', op_dtypes=[np.dtype('f4')])
    with it:
        it.operands[0][:] = 100
    assert_equal(au, 100)
    # do it again, this time raise an error,
    it = nditer(au, [], [['readwrite', 'updateifcopy']],
                        casting='equiv', op_dtypes=[np.dtype('f4')])
    try:
        with it:
            assert_equal(au.flags.writeable, False)
            it.operands[0][:] = 0
            raise ValueError('exit context manager on exception')
    except Exception:
        pass
    assert_equal(au, 0)
    assert_equal(au.flags.writeable, True)
    # cannot reuse i outside context manager
    assert_raises(ValueError, getattr, it, 'operands')

    it = nditer(au, [], [['readwrite', 'updateifcopy']],
                        casting='equiv', op_dtypes=[np.dtype('f4')])
    with it:
        x = it.operands[0]
        x[:] = 6
        assert_(x.flags.writebackifcopy)
    assert_equal(au, 6)
    assert_(not x.flags.writebackifcopy)
    x[:] = 123  # x.data still valid
    assert_equal(au, 6)  # but not connected to au

    it = nditer(au, [],
                 [['readwrite', 'updateifcopy']],
                 casting='equiv', op_dtypes=[np.dtype('f4')])
    # reentering works
    with it:
        with it:
            for x in it:
                x[...] = 123

    it = nditer(au, [],
                 [['readwrite', 'updateifcopy']],
                 casting='equiv', op_dtypes=[np.dtype('f4')])
    # make sure exiting the inner context manager closes the iterator
    with it:
        with it:
            for x in it:
                x[...] = 123
        assert_raises(ValueError, getattr, it, 'operands')
    # do not crash if original data array is decrefed
    it = nditer(au, [],
                 [['readwrite', 'updateifcopy']],
                 casting='equiv', op_dtypes=[np.dtype('f4')])
    del au
    with it:
        for x in it:
            x[...] = 123
    # make sure we cannot reenter the closed iterator
    enter = it.__enter__
    assert_raises(RuntimeError, enter)

