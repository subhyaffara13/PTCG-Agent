
def test_default_is_matrix_spdiags():
    m = scipy.sparse.spdiags([1.0, 2.0, 3.0], 0, 3, 3)
    assert not isinstance(m, scipy.sparse.sparray)

