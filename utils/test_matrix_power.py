
def test_matrix_power():
    np.random.seed(1234)
    row, col = np.random.randint(0, 4, size=(2, 6))
    data = np.random.random(size=(6,))
    Amat = csc_array((data, (row, col)), shape=(4, 4))
    A = csc_array((data, (row, col)), shape=(4, 4))
    Adense = A.toarray()
    for power in (2, 5, 6):
        Apow = matrix_power(A, power).toarray()
        Amat_pow = matrix_power(Amat, power).toarray()
        Adense_pow = np.linalg.matrix_power(Adense, power)
        assert_allclose(Apow, Adense_pow)
        assert_allclose(Apow, Amat_pow)


def test_matrix_power():
    A = matrix([[1, 2], [3, 4]])
    assert A**2 == A*A
    assert A**3 == A*A*A
    assert A**-1 == inverse(A)
    assert A**-2 == inverse(A*A)

