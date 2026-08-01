
def test_iter_nbo_align_contig():
    # Check that byte order, alignment, and contig changes work

    # Byte order change by requesting a specific dtype
    a = np.arange(6, dtype='f4')
    au = a.byteswap()
    au = au.view(au.dtype.newbyteorder())
    assert_(a.dtype.byteorder != au.dtype.byteorder)
    i = nditer(au, [], [['readwrite', 'updateifcopy']],
                        casting='equiv',
                        op_dtypes=[np.dtype('f4')])
    with i:
        # context manager triggers WRITEBACKIFCOPY on i at exit
        assert_equal(i.dtypes[0].byteorder, a.dtype.byteorder)
        assert_equal(i.operands[0].dtype.byteorder, a.dtype.byteorder)
        assert_equal(i.operands[0], a)
        i.operands[0][:] = 2
    assert_equal(au, [2] * 6)
    del i  # should not raise a warning
    # Byte order change by requesting NBO
    a = np.arange(6, dtype='f4')
    au = a.byteswap()
    au = au.view(au.dtype.newbyteorder())
    assert_(a.dtype.byteorder != au.dtype.byteorder)
    with nditer(au, [], [['readwrite', 'updateifcopy', 'nbo']],
                        casting='equiv') as i:
        # context manager triggers UPDATEIFCOPY on i at exit
        assert_equal(i.dtypes[0].byteorder, a.dtype.byteorder)
        assert_equal(i.operands[0].dtype.byteorder, a.dtype.byteorder)
        assert_equal(i.operands[0], a)
        i.operands[0][:] = 12345
        i.operands[0][:] = 2
    assert_equal(au, [2] * 6)

    # Unaligned input
    a = np.zeros((6 * 4 + 1,), dtype='i1')[1:]
    a = a.view('f4')
    a[:] = np.arange(6, dtype='f4')
    assert_(not a.flags.aligned)
    # Without 'aligned', shouldn't copy
    i = nditer(a, [], [['readonly']])
    assert_(not i.operands[0].flags.aligned)
    assert_equal(i.operands[0], a)
    # With 'aligned', should make a copy
    with nditer(a, [], [['readwrite', 'updateifcopy', 'aligned']]) as i:
        assert_(i.operands[0].flags.aligned)
        # context manager triggers UPDATEIFCOPY on i at exit
        assert_equal(i.operands[0], a)
        i.operands[0][:] = 3
    assert_equal(a, [3] * 6)

    # Discontiguous input
    a = arange(12)
    # If it is contiguous, shouldn't copy
    i = nditer(a[:6], [], [['readonly']])
    assert_(i.operands[0].flags.contiguous)
    assert_equal(i.operands[0], a[:6])
    # If it isn't contiguous, should buffer
    i = nditer(a[::2], ['buffered', 'external_loop'],
                        [['readonly', 'contig']],
                        buffersize=10)
    assert_(i[0].flags.contiguous)
    assert_equal(i[0], a[::2])

