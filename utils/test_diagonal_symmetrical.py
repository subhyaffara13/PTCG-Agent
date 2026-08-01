
def test_diagonal_symmetrical():
    m = PropertiesOnlyMatrix(2, 2, [0, 1, 1, 0])
    assert not m.is_diagonal()
    assert m.is_symmetric()
    assert m.is_symmetric(simplify=False)

    m = PropertiesOnlyMatrix(2, 2, [1, 0, 0, 1])
    assert m.is_diagonal()

    m = PropertiesOnlyMatrix(3, 3, diag(1, 2, 3))
    assert m.is_diagonal()
    assert m.is_symmetric()

    m = PropertiesOnlyMatrix(3, 3, [1, 0, 0, 0, 2, 0, 0, 0, 3])
    assert m == diag(1, 2, 3)

    m = PropertiesOnlyMatrix(2, 3, zeros(2, 3))
    assert not m.is_symmetric()
    assert m.is_diagonal()

    m = PropertiesOnlyMatrix(((5, 0), (0, 6), (0, 0)))
    assert m.is_diagonal()

    m = PropertiesOnlyMatrix(((5, 0, 0), (0, 6, 0)))
    assert m.is_diagonal()

    m = Matrix(3, 3, [1, x**2 + 2*x + 1, y, (x + 1)**2, 2, 0, y, 0, 3])
    assert m.is_symmetric()
    assert not m.is_symmetric(simplify=False)
    assert m.expand().is_symmetric(simplify=False)


def test_diagonal_symmetrical():
    m = Matrix(2, 2, [0, 1, 1, 0])
    assert not m.is_diagonal()
    assert m.is_symmetric()
    assert m.is_symmetric(simplify=False)

    m = Matrix(2, 2, [1, 0, 0, 1])
    assert m.is_diagonal()

    m = diag(1, 2, 3)
    assert m.is_diagonal()
    assert m.is_symmetric()

    m = Matrix(3, 3, [1, 0, 0, 0, 2, 0, 0, 0, 3])
    assert m == diag(1, 2, 3)

    m = Matrix(2, 3, zeros(2, 3))
    assert not m.is_symmetric()
    assert m.is_diagonal()

    m = Matrix(((5, 0), (0, 6), (0, 0)))
    assert m.is_diagonal()

    m = Matrix(((5, 0, 0), (0, 6, 0)))
    assert m.is_diagonal()

    m = Matrix(3, 3, [1, x**2 + 2*x + 1, y, (x + 1)**2, 2, 0, y, 0, 3])
    assert m.is_symmetric()
    assert not m.is_symmetric(simplify=False)
    assert m.expand().is_symmetric(simplify=False)


def test_diagonal_symmetrical():
    m = Matrix(2, 2, [0, 1, 1, 0])
    assert not m.is_diagonal()
    assert m.is_symmetric()
    assert m.is_symmetric(simplify=False)

    m = Matrix(2, 2, [1, 0, 0, 1])
    assert m.is_diagonal()

    m = diag(1, 2, 3)
    assert m.is_diagonal()
    assert m.is_symmetric()

    m = Matrix(3, 3, [1, 0, 0, 0, 2, 0, 0, 0, 3])
    assert m == diag(1, 2, 3)

    m = Matrix(2, 3, zeros(2, 3))
    assert not m.is_symmetric()
    assert m.is_diagonal()

    m = Matrix(((5, 0), (0, 6), (0, 0)))
    assert m.is_diagonal()

    m = Matrix(((5, 0, 0), (0, 6, 0)))
    assert m.is_diagonal()

    m = Matrix(3, 3, [1, x**2 + 2*x + 1, y, (x + 1)**2, 2, 0, y, 0, 3])
    assert m.is_symmetric()
    assert not m.is_symmetric(simplify=False)
    assert m.expand().is_symmetric(simplify=False)

