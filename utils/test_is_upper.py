
def test_is_upper():
    a = PropertiesOnlyMatrix([[1, 2, 3]])
    assert a.is_upper is True
    a = PropertiesOnlyMatrix([[1], [2], [3]])
    assert a.is_upper is False


def test_is_upper():
    a = Matrix([[1, 2, 3]])
    assert a.is_upper is True
    a = Matrix([[1], [2], [3]])
    assert a.is_upper is False
    a = zeros(4, 2)
    assert a.is_upper is True


def test_is_upper():
    a = Matrix([[1, 2, 3]])
    assert a.is_upper is True
    a = Matrix([[1], [2], [3]])
    assert a.is_upper is False
    a = zeros(4, 2)
    assert a.is_upper is True

