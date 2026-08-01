
def test_diag():
    # mostly tested in testcommonmatrix.py
    assert diag([1, 2, 3]) == Matrix([1, 2, 3])
    m = [1, 2, [3]]
    raises(ValueError, lambda: diag(m))
    assert diag(m, strict=False) == Matrix([1, 2, 3])


def test_diag():
    # mostly tested in testcommonmatrix.py
    assert diag([1, 2, 3]) == Matrix([1, 2, 3])
    m = [1, 2, [3]]
    raises(ValueError, lambda: diag(m))
    assert diag(m, strict=False) == Matrix([1, 2, 3])

