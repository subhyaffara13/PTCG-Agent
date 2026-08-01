
def test_is_lower():
    a = PropertiesOnlyMatrix([[1, 2, 3]])
    assert a.is_lower is False
    a = PropertiesOnlyMatrix([[1], [2], [3]])
    assert a.is_lower is True


def test_is_lower():
    a = Matrix([[1, 2, 3]])
    assert a.is_lower is False
    a = Matrix([[1], [2], [3]])
    assert a.is_lower is True


def test_is_lower():
    a = Matrix([[1, 2, 3]])
    assert a.is_lower is False
    a = Matrix([[1], [2], [3]])
    assert a.is_lower is True

