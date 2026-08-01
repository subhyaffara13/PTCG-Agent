
def test_iter_buffering():
    # Test buffering with several buffer sizes and types
    arrays = []
    # F-order swapped array
    _tmp = np.arange(24, dtype='c16').reshape(2, 3, 4).T
    _tmp = _tmp.view(_tmp.dtype.newbyteorder()).byteswap()
    arrays.append(_tmp)
    # Contiguous 1-dimensional array
    arrays.append(np.arange(10, dtype='f4'))
    # Unaligned array
    a = np.zeros((4 * 16 + 1,), dtype='i1')[1:]
    a = a.view('i4')
    a[:] = np.arange(16, dtype='i4')
    arrays.append(a)
    # 4-D F-order array
    arrays.append(np.arange(120, dtype='i4').reshape(5, 3, 2, 4).T)
    for a in arrays:
        for buffersize in (1, 2, 3, 5, 8, 11, 16, 1024):
            vals = []
            i = nditer(a, ['buffered', 'external_loop'],
                           [['readonly', 'nbo', 'aligned']],
                           order='C',
                           casting='equiv',
                           buffersize=buffersize)
            while not i.finished:
                assert_(i[0].size <= buffersize)
                vals.append(i[0].copy())
                i.iternext()
            assert_equal(np.concatenate(vals), a.ravel(order='C'))

