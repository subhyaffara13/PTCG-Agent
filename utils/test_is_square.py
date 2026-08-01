
def test_is_square():
    assert [i for i in range(25) if is_square(i)] == [0, 1, 4, 9, 16]

    # issue #17044
    assert not is_square(60 ** 3)
    assert not is_square(60 ** 5)
    assert not is_square(84 ** 7)
    assert not is_square(105 ** 9)
    assert not is_square(120 ** 3)


def test_is_square():
    m = PropertiesOnlyMatrix([[1], [1]])
    m2 = PropertiesOnlyMatrix([[2, 2], [2, 2]])
    assert not m.is_square
    assert m2.is_square


def test_is_square():
    m = Matrix([[1], [1]])
    m2 = Matrix([[2, 2], [2, 2]])
    assert not m.is_square
    assert m2.is_square

