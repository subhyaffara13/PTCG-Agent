
def test_iter_iterindex():
    # Make sure iterindex works

    buffersize = 5
    a = arange(24).reshape(4, 3, 2)
    for flags in ([], ['buffered']):
        i = nditer(a, flags, buffersize=buffersize)
        assert_equal(iter_iterindices(i), list(range(24)))
        i.iterindex = 2
        assert_equal(iter_iterindices(i), list(range(2, 24)))

        i = nditer(a, flags, order='F', buffersize=buffersize)
        assert_equal(iter_iterindices(i), list(range(24)))
        i.iterindex = 5
        assert_equal(iter_iterindices(i), list(range(5, 24)))

        i = nditer(a[::-1], flags, order='F', buffersize=buffersize)
        assert_equal(iter_iterindices(i), list(range(24)))
        i.iterindex = 9
        assert_equal(iter_iterindices(i), list(range(9, 24)))

        i = nditer(a[::-1, ::-1], flags, order='C', buffersize=buffersize)
        assert_equal(iter_iterindices(i), list(range(24)))
        i.iterindex = 13
        assert_equal(iter_iterindices(i), list(range(13, 24)))

        i = nditer(a[::1, ::-1], flags, buffersize=buffersize)
        assert_equal(iter_iterindices(i), list(range(24)))
        i.iterindex = 23
        assert_equal(iter_iterindices(i), list(range(23, 24)))
        i.reset()
        i.iterindex = 2
        assert_equal(iter_iterindices(i), list(range(2, 24)))

