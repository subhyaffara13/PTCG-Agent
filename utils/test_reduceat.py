
def test_reduceat():
    """Test bug in reduceat when structured arrays are not copied."""
    db = np.dtype([('name', 'S11'), ('time', np.int64), ('value', np.float32)])
    a = np.empty([100], dtype=db)
    a['name'] = 'Simple'
    a['time'] = 10
    a['value'] = 100
    indx = [0, 7, 15, 25]

    h2 = []
    val1 = indx[0]
    for val2 in indx[1:]:
        h2.append(np.add.reduce(a['value'][val1:val2]))
        val1 = val2
    h2.append(np.add.reduce(a['value'][val1:]))
    h2 = np.array(h2)

    # test buffered -- this should work
    h1 = np.add.reduceat(a['value'], indx)
    assert_array_almost_equal(h1, h2)

    # This is when the error occurs.
    # test no buffer
    np.setbufsize(32)
    h1 = np.add.reduceat(a['value'], indx)
    np.setbufsize(ncu.UFUNC_BUFSIZE_DEFAULT)
    assert_array_almost_equal(h1, h2)

