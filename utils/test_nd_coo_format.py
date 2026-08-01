
def test_nd_coo_format(ndim, value):
    A = coo_array([value]).reshape((1,) * ndim)

    #save/load array
    fd, tmpfile = tempfile.mkstemp(suffix='.npz')
    os.close(fd)
    try:
        save_npz(tmpfile, A)
        loaded_A = load_npz(tmpfile)
    finally:
        os.remove(tmpfile)

    assert isinstance(loaded_A, coo_array)
    assert_(loaded_A.shape == A.shape)
    assert_equal(A.toarray(), loaded_A.toarray())

