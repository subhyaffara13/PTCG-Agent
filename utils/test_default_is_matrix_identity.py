
def test_default_is_matrix_identity():
    m = scipy.sparse.identity(3)
    assert not isinstance(m, scipy.sparse.sparray)

