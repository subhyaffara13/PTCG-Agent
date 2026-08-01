
def test_default_is_matrix_diags():
    m = scipy.sparse.diags([0.0, 1.0, 2.0])
    assert not isinstance(m, scipy.sparse.sparray)

