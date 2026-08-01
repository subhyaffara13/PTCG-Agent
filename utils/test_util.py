
def test_util():
    R = Rational

    v1 = Matrix(1, 3, [1, 2, 3])
    v2 = Matrix(1, 3, [3, 4, 5])
    assert v1.norm() == sqrt(14)
    assert v1.project(v2) == Matrix(1, 3, [R(39)/25, R(52)/25, R(13)/5])
    assert Matrix.zeros(1, 2) == Matrix(1, 2, [0, 0])
    assert ones(1, 2) == Matrix(1, 2, [1, 1])
    assert v1.copy() == v1
    # cofactor
    assert eye(3) == eye(3).cofactor_matrix()
    test = Matrix([[1, 3, 2], [2, 6, 3], [2, 3, 6]])
    assert test.cofactor_matrix() == \
        Matrix([[27, -6, -6], [-12, 2, 3], [-3, 1, 0]])
    test = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert test.cofactor_matrix() == \
        Matrix([[-3, 6, -3], [6, -12, 6], [-3, 6, -3]])

