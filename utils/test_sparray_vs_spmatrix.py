import os

def test_sparray_vs_spmatrix():
    #save/load matrix
    fd, tmpfile = tempfile.mkstemp(suffix='.npz')
    os.close(fd)
    try:
        save_npz(tmpfile, csr_matrix([[1.2, 0, 0.9], [0, 0.3, 0]]))
        loaded_matrix = load_npz(tmpfile)
    finally:
        os.remove(tmpfile)

    #save/load array
    fd, tmpfile = tempfile.mkstemp(suffix='.npz')
    os.close(fd)
    try:
        save_npz(tmpfile, csr_array([[1.2, 0, 0.9], [0, 0.3, 0]]))
        loaded_array = load_npz(tmpfile)
    finally:
        os.remove(tmpfile)

    assert not isinstance(loaded_matrix, sparray)
    assert isinstance(loaded_array, sparray)
    assert_(loaded_matrix.dtype == loaded_array.dtype)
    assert_equal(loaded_matrix.toarray(), loaded_array.toarray())

