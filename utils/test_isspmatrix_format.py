
def test_isspmatrix_format(fmt, fn):
    m = scipy.sparse.eye(3, format=fmt)
    a = scipy.sparse.csr_array(m).asformat(fmt)
    assert not isinstance(m, scipy.sparse.sparray)
    assert isinstance(a, scipy.sparse.sparray)

    # Should only be true for sparse matrices, not sparse arrays
    assert not fn(a)
    assert fn(m)

    # ndarray and array_likes are not sparse
    assert not fn(a.todense())
    assert not fn(m.todense())

