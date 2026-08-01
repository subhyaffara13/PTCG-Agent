
def test_default_is_matrix_eye():
    m = scipy.sparse.eye(3)
    assert not isinstance(m, scipy.sparse.sparray)

