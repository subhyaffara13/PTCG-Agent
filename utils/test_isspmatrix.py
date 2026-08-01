
def test_isspmatrix():
    m = scipy.sparse.eye(3)
    a = scipy.sparse.csr_array(m)
    assert not isinstance(m, scipy.sparse.sparray)
    assert isinstance(a, scipy.sparse.sparray)

    # Should only be true for sparse matrices, not sparse arrays
    assert not scipy.sparse.isspmatrix(a)
    assert scipy.sparse.isspmatrix(m)

    # ndarray and array_likes are not sparse
    assert not scipy.sparse.isspmatrix(a.todense())
    assert not scipy.sparse.isspmatrix(m.todense())

