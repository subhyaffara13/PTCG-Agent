
def test_default_is_matrix_random():
    m = scipy.sparse.random(3, 3)
    assert not isinstance(m, scipy.sparse.sparray)

