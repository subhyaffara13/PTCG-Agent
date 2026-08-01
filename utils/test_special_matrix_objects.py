
def test_special_matrix_objects():
    assert np.all(m.incr_diag(7) == np.diag([1.0, 2, 3, 4, 5, 6, 7]))

    asymm = np.array([[1.0, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
    symm_lower = np.array(asymm)
    symm_upper = np.array(asymm)
    for i in range(4):
        for j in range(i + 1, 4):
            symm_lower[i, j] = symm_lower[j, i]
            symm_upper[j, i] = symm_upper[i, j]

    assert np.all(m.symmetric_lower(asymm) == symm_lower)
    assert np.all(m.symmetric_upper(asymm) == symm_upper)

