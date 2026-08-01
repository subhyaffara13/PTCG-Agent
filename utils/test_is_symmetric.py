
def test_is_symmetric():
    m = PropertiesOnlyMatrix(2, 2, [0, 1, 1, 0])
    assert m.is_symmetric()
    m = PropertiesOnlyMatrix(2, 2, [0, 1, 0, 1])
    assert not m.is_symmetric()


def test_is_symmetric():
    m = Matrix(2, 2, [0, 1, 1, 0])
    assert m.is_symmetric()
    m = Matrix(2, 2, [0, 1, 0, 1])
    assert not m.is_symmetric()


def test_is_symmetric():
    a = Permutation(0, 1, 2)
    b = Permutation(0, 1, size=3)
    assert PermutationGroup(a, b).is_symmetric is True

    a = Permutation(0, 2, 1)
    b = Permutation(1, 2, size=3)
    assert PermutationGroup(a, b).is_symmetric is True

    a = Permutation(0, 1, 2, 3)
    b = Permutation(0, 3)(1, 2)
    assert PermutationGroup(a, b).is_symmetric is False

