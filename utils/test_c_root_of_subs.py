
def test_CRootOf_subs():
    assert rootof(x**3 + x + 1, 0).subs(x, y) == rootof(y**3 + y + 1, 0)

