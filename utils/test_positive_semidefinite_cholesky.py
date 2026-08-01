
def test_positive_semidefinite_cholesky():
    from sympy.matrices.eigen import _is_positive_semidefinite_cholesky

    m = Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    assert _is_positive_semidefinite_cholesky(m) == True
    m = Matrix([[0, 0, 0], [0, 5, -10*I], [0, 10*I, 5]])
    assert _is_positive_semidefinite_cholesky(m) == False
    m = Matrix([[1, 0, 0], [0, 0, 0], [0, 0, -1]])
    assert _is_positive_semidefinite_cholesky(m) == False
    m = Matrix([[0, 1], [1, 0]])
    assert _is_positive_semidefinite_cholesky(m) == False

    # https://www.value-at-risk.net/cholesky-factorization/
    m = Matrix([[4, -2, -6], [-2, 10, 9], [-6, 9, 14]])
    assert _is_positive_semidefinite_cholesky(m) == True
    m = Matrix([[9, -3, 3], [-3, 2, 1], [3, 1, 6]])
    assert _is_positive_semidefinite_cholesky(m) == True
    m = Matrix([[4, -2, 2], [-2, 1, -1], [2, -1, 5]])
    assert _is_positive_semidefinite_cholesky(m) == True
    m = Matrix([[1, 2, -1], [2, 5, 1], [-1, 1, 9]])
    assert _is_positive_semidefinite_cholesky(m) == False

