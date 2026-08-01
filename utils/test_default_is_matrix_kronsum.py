
def test_default_is_matrix_kronsum():
    m = scipy.sparse.kronsum(
        np.array([[1, 0], [0, 1]]), np.array([[0, 1], [1, 0]])
    )
    assert not isinstance(m, scipy.sparse.sparray)

