
def test_matrix_to_density():
    mat = Matrix([[0, 0], [0, 1]])
    assert matrix_to_density(mat) == Density([Qubit('1'), 1])

    mat = Matrix([[1, 0], [0, 0]])
    assert matrix_to_density(mat) == Density([Qubit('0'), 1])

    mat = Matrix([[0, 0], [0, 0]])
    assert matrix_to_density(mat) == 0

    mat = Matrix([[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 0]])

    assert matrix_to_density(mat) == Density([Qubit('10'), 1])

    mat = Matrix([[1, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]])

    assert matrix_to_density(mat) == Density([Qubit('00'), 1])

