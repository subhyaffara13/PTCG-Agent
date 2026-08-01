
def test_issparse():
    m = scipy.sparse.eye(3)
    a = scipy.sparse.csr_array(m)
    assert not isinstance(m, scipy.sparse.sparray)
    assert isinstance(a, scipy.sparse.sparray)

    # Both sparse arrays and sparse matrices should be sparse
    assert scipy.sparse.issparse(a)
    assert scipy.sparse.issparse(m)

    # ndarray and array_likes are not sparse
    assert not scipy.sparse.issparse(a.todense())
    assert not scipy.sparse.issparse(m.todense())

