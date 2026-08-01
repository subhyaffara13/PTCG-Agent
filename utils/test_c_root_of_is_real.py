
def test_CRootOf_is_real():
    assert rootof(x**3 + x + 3, 0).is_real is True
    assert rootof(x**3 + x + 3, 1).is_real is False
    assert rootof(x**3 + x + 3, 2).is_real is False

