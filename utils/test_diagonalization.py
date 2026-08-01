
def test_diagonalization():
    m = Matrix([[1, 2+I], [2-I, 3]])
    assert m.is_diagonalizable()

    m = Matrix(3, 2, [-3, 1, -3, 20, 3, 10])
    assert not m.is_diagonalizable()
    assert not m.is_symmetric()
    raises(NonSquareMatrixError, lambda: m.diagonalize())

    # diagonalizable
    m = diag(1, 2, 3)
    (P, D) = m.diagonalize()
    assert P == eye(3)
    assert D == m

    m = Matrix(2, 2, [0, 1, 1, 0])
    assert m.is_symmetric()
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D

    m = Matrix(2, 2, [1, 0, 0, 3])
    assert m.is_symmetric()
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D
    assert P == eye(2)
    assert D == m

    m = Matrix(2, 2, [1, 1, 0, 0])
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D

    m = Matrix(3, 3, [1, 2, 0, 0, 3, 0, 2, -4, 2])
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D
    for i in P:
        assert i.as_numer_denom()[1] == 1

    m = Matrix(2, 2, [1, 0, 0, 0])
    assert m.is_diagonal()
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D
    assert P == Matrix([[0, 1], [1, 0]])

    # diagonalizable, complex only
    m = Matrix(2, 2, [0, 1, -1, 0])
    assert not m.is_diagonalizable(True)
    raises(MatrixError, lambda: m.diagonalize(True))
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D

    # not diagonalizable
    m = Matrix(2, 2, [0, 1, 0, 0])
    assert not m.is_diagonalizable()
    raises(MatrixError, lambda: m.diagonalize())

    m = Matrix(3, 3, [-3, 1, -3, 20, 3, 10, 2, -2, 4])
    assert not m.is_diagonalizable()
    raises(MatrixError, lambda: m.diagonalize())

    # symbolic
    a, b, c, d = symbols('a b c d')
    m = Matrix(2, 2, [a, c, c, b])
    assert m.is_symmetric()
    assert m.is_diagonalizable()


def test_diagonalization():
    m = Matrix([[1, 2+I], [2-I, 3]])
    assert m.is_diagonalizable()

    m = Matrix(3, 2, [-3, 1, -3, 20, 3, 10])
    assert not m.is_diagonalizable()
    assert not m.is_symmetric()
    raises(NonSquareMatrixError, lambda: m.diagonalize())

    # diagonalizable
    m = diag(1, 2, 3)
    (P, D) = m.diagonalize()
    assert P == eye(3)
    assert D == m

    m = Matrix(2, 2, [0, 1, 1, 0])
    assert m.is_symmetric()
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D

    m = Matrix(2, 2, [1, 0, 0, 3])
    assert m.is_symmetric()
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D
    assert P == eye(2)
    assert D == m

    m = Matrix(2, 2, [1, 1, 0, 0])
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D

    m = Matrix(3, 3, [1, 2, 0, 0, 3, 0, 2, -4, 2])
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D
    for i in P:
        assert i.as_numer_denom()[1] == 1

    m = Matrix(2, 2, [1, 0, 0, 0])
    assert m.is_diagonal()
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D
    assert P == Matrix([[0, 1], [1, 0]])

    # diagonalizable, complex only
    m = Matrix(2, 2, [0, 1, -1, 0])
    assert not m.is_diagonalizable(True)
    raises(MatrixError, lambda: m.diagonalize(True))
    assert m.is_diagonalizable()
    (P, D) = m.diagonalize()
    assert P.inv() * m * P == D

    # not diagonalizable
    m = Matrix(2, 2, [0, 1, 0, 0])
    assert not m.is_diagonalizable()
    raises(MatrixError, lambda: m.diagonalize())

    m = Matrix(3, 3, [-3, 1, -3, 20, 3, 10, 2, -2, 4])
    assert not m.is_diagonalizable()
    raises(MatrixError, lambda: m.diagonalize())

    # symbolic
    a, b, c, d = symbols('a b c d')
    m = Matrix(2, 2, [a, c, c, b])
    assert m.is_symmetric()
    assert m.is_diagonalizable()

