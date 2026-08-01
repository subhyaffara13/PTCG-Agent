
def test_iter_write_buffering():
    # Test that buffering of writes is working

    # F-order swapped array
    a = np.arange(24).reshape(2, 3, 4).T
    a = a.view(a.dtype.newbyteorder()).byteswap()
    i = nditer(a, ['buffered'],
                   [['readwrite', 'nbo', 'aligned']],
                   casting='equiv',
                   order='C',
                   buffersize=16)
    x = 0
    with i:
        while not i.finished:
            i[0] = x
            x += 1
            i.iternext()
    assert_equal(a.ravel(order='C'), np.arange(24))

