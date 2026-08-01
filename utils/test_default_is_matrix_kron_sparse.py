
def test_default_is_matrix_kron_sparse():
    m = scipy.sparse.kron(
        np.array([[1, 2], [3, 4]]), np.array([[1, 0], [0, 0]])
    )
    assert not isinstance(m, scipy.sparse.sparray)

