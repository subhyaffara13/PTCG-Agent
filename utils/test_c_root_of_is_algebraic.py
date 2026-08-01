
def test_CRootOf_is_algebraic():
    assert rootof(x**3 + x + 3, 0).is_algebraic is True
    assert rootof(x**3 + x + 3, 1).is_algebraic is True
    assert rootof(x**3 + x + 3, 2).is_algebraic is True

