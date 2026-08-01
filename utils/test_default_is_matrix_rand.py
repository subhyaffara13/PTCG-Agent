
def test_default_is_matrix_rand():
    m = scipy.sparse.rand(3, 3)
    assert not isinstance(m, scipy.sparse.sparray)

