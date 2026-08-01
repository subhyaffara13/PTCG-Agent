
def test_CRootOf_diff():
    assert rootof(x**3 + x + 1, 0).diff(x) == 0
    assert rootof(x**3 + x + 1, 0).diff(y) == 0

