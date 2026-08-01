
def test_is_symbolic():
    a = PropertiesOnlyMatrix([[x, x], [x, x]])
    assert a.is_symbolic() is True
    a = PropertiesOnlyMatrix([[1, 2, 3, 4], [5, 6, 7, 8]])
    assert a.is_symbolic() is False
    a = PropertiesOnlyMatrix([[1, 2, 3, 4], [5, 6, x, 8]])
    assert a.is_symbolic() is True
    a = PropertiesOnlyMatrix([[1, x, 3]])
    assert a.is_symbolic() is True
    a = PropertiesOnlyMatrix([[1, 2, 3]])
    assert a.is_symbolic() is False
    a = PropertiesOnlyMatrix([[1], [x], [3]])
    assert a.is_symbolic() is True
    a = PropertiesOnlyMatrix([[1], [2], [3]])
    assert a.is_symbolic() is False


def test_is_symbolic():
    a = Matrix([[x, x], [x, x]])
    assert a.is_symbolic() is True
    a = Matrix([[1, 2, 3, 4], [5, 6, 7, 8]])
    assert a.is_symbolic() is False
    a = Matrix([[1, 2, 3, 4], [5, 6, x, 8]])
    assert a.is_symbolic() is True
    a = Matrix([[1, x, 3]])
    assert a.is_symbolic() is True
    a = Matrix([[1, 2, 3]])
    assert a.is_symbolic() is False
    a = Matrix([[1], [x], [3]])
    assert a.is_symbolic() is True
    a = Matrix([[1], [2], [3]])
    assert a.is_symbolic() is False


def test_is_symbolic():
    a = Matrix([[x, x], [x, x]])
    assert a.is_symbolic() is True
    a = Matrix([[1, 2, 3, 4], [5, 6, 7, 8]])
    assert a.is_symbolic() is False
    a = Matrix([[1, 2, 3, 4], [5, 6, x, 8]])
    assert a.is_symbolic() is True
    a = Matrix([[1, x, 3]])
    assert a.is_symbolic() is True
    a = Matrix([[1, 2, 3]])
    assert a.is_symbolic() is False
    a = Matrix([[1], [x], [3]])
    assert a.is_symbolic() is True
    a = Matrix([[1], [2], [3]])
    assert a.is_symbolic() is False

