
def test_default_is_matrix_kron_dense():
    m = scipy.sparse.kron(
        np.array([[1, 2], [3, 4]]), np.array([[4, 3], [2, 1]])
    )
    assert not isinstance(m, scipy.sparse.sparray)

